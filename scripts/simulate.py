#!/usr/bin/env python3
"""
Live-dashboard data simulator.

Seeds one terminal + 3 zones + 4 employees + 3 cameras, then continuously
sends sensor positions (every second) and camera events (every 3 seconds)
so the live-dashboard has real-looking data.

Usage:
    python scripts/simulate.py
    python scripts/simulate.py --url http://localhost:8000/api
    python scripts/simulate.py --interval 2   # slower tick

Requirements: Python 3.11+ stdlib only (no pip install needed).
"""
import argparse
import json
import random
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Static layout — pixel coords matching the 800×600 map overlay
# ---------------------------------------------------------------------------
ZONES_DEF = [
    {"name": "Loading Bay A", "points": [[50, 50],  [350, 50],  [350, 280], [50, 280]]},
    {"name": "Storage B",     "points": [[420, 50], [750, 50],  [750, 280], [420, 280]]},
    {"name": "Dispatch C",    "points": [[50, 340], [550, 340], [550, 560], [50, 560]]},
]

EMPLOYEE_NAMES = [
    "Ivan Petrenko",
    "Olena Kovalenko",
    "Mykola Shevchenko",
    "Sofia Bondarenko",
]

ACTION_TYPES = ["loading", "unloading", "idle", "scanning", "moving"]


# ---------------------------------------------------------------------------
# Minimal HTTP helpers (stdlib only)
# ---------------------------------------------------------------------------
def _request(method: str, url: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} {method} {url}: {e.read().decode()}") from e
    except urllib.error.URLError as e:
        raise ConnectionError(f"Cannot reach {url}: {e.reason}") from e


def get(base: str, path: str) -> list | dict:
    return _request("GET", f"{base}{path}")


def post(base: str, path: str, body: dict) -> dict:
    return _request("POST", f"{base}{path}", body)


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------
def zone_center(points: list) -> tuple[float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0


def clamp_to_zone(x: float, y: float, points: list, margin: float = 20) -> tuple[float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x = max(min(xs) + margin, min(max(xs) - margin, x))
    y = max(min(ys) + margin, min(max(ys) - margin, y))
    return x, y


# ---------------------------------------------------------------------------
# Seeding (idempotent — reuses Terminal-SIM if it already exists)
# ---------------------------------------------------------------------------
def seed(base: str) -> tuple[list, list, list]:
    # Check for existing Terminal-SIM
    existing = get(base, "/terminals/")
    terminal = next((t for t in existing if t["name"] == "Terminal-SIM"), None)

    if terminal:
        tid = terminal["id"]
        print(f"Reusing existing Terminal-SIM id={tid}")

        raw_zones = get(base, f"/terminals/{tid}/zones/")
        zones = []
        for z_api in raw_zones:
            match = next((z for z in ZONES_DEF if z["name"] == z_api["name"]), None)
            z_api["_points"] = match["points"] if match else ZONES_DEF[0]["points"]
            zones.append(z_api)
            print(f"  Zone  '{z_api['name']}' id={z_api['id']} (reused)")

        cameras = get(base, "/cameras/")
        cameras = [c for c in cameras if c["terminal_id"] == tid]
        print(f"  {len(cameras)} camera(s) reused")

        employees_all = get(base, "/employees/")
        employees = [e for e in employees_all if e["terminal_id"] == tid]
        print(f"  {len(employees)} employee(s) reused")

        if not zones or not cameras or not employees:
            print("  Incomplete seed data — re-seeding missing pieces…")
            zones, cameras, employees = _create_seed(base, tid, zones, cameras, employees)

        return zones, cameras, employees

    print("Seeding fresh data…")
    terminal = post(base, "/terminals/", {"name": "Terminal-SIM", "description": "Simulation terminal"})
    tid = terminal["id"]
    print(f"  Terminal id={tid}")
    return _create_seed(base, tid, [], [], [])


def _create_seed(
    base: str, tid: int,
    existing_zones: list, existing_cameras: list, existing_employees: list,
) -> tuple[list, list, list]:
    run_id = int(time.time())

    zones = existing_zones or []
    if not zones:
        for z in ZONES_DEF:
            zone = post(base, f"/terminals/{tid}/zones/", {"name": z["name"], "points": z["points"]})
            zone["_points"] = z["points"]
            zones.append(zone)
            print(f"  Zone  '{zone['name']}' id={zone['id']}")

    cameras = existing_cameras or []
    if not cameras:
        for i, zone in enumerate(zones):
            cam = post(base, "/cameras/", {
                "name": f"Cam-{i + 1}",
                "stream_url": f"rtsp://sim/cam{i + 1}",
                "mac_address": f"AA:BB:CC:DD:EE:{i:02X}",
                "version": "1.0.0",
                "location": f"Zone entrance {i + 1}",
                "terminal_id": tid,
                "zone_id": zone["id"],
            })
            cameras.append(cam)
            print(f"  Camera '{cam['name']}' id={cam['id']} → zone {zone['id']}")

    employees = existing_employees or []
    if not employees:
        for i, name in enumerate(EMPLOYEE_NAMES):
            emp = post(base, "/employees/", {
                "name": name,
                "badge_id": f"SIM-{run_id}-{i}",
                "terminal_id": tid,
            })
            employees.append(emp)
            print(f"  Employee '{emp['name']}' id={emp['id']}")

    return zones, cameras, employees


# ---------------------------------------------------------------------------
# Simulation loop
# ---------------------------------------------------------------------------
def simulate(base: str, zones: list, cameras: list, employees: list, interval: float) -> None:
    # Assign each employee to a zone + camera (round-robin)
    assignments = [
        (emp, zones[i % len(zones)], cameras[i % len(cameras)])
        for i, emp in enumerate(employees)
    ]

    # Start each employee at their zone's center
    positions: dict[int, list[float]] = {
        emp["id"]: list(zone_center(zone["_points"]))
        for emp, zone, _ in assignments
    }

    tick = 0
    print(f"\nSimulating {len(employees)} employees across {len(zones)} zones "
          f"(tick every {interval}s)  —  Ctrl+C to stop\n")

    while True:
        now = datetime.now(timezone.utc).isoformat()

        # ── sensor positions ──────────────────────────────────────────────
        for emp, zone, cam in assignments:
            eid = emp["id"]
            px, py = positions[eid]
            px += random.uniform(-12, 12)
            py += random.uniform(-12, 12)
            px, py = clamp_to_zone(px, py, zone["_points"])
            positions[eid] = [px, py]

            try:
                post(base, "/sensor-positions/", {
                    "employee_id": eid,
                    "x": round(px, 1),
                    "y": round(py, 1),
                    "timestamp": now,
                })
                print(f"  [pos] {emp['name']:<22} ({px:6.1f},{py:6.1f})  zone={zone['name']}")
            except Exception as exc:
                print(f"  [pos] ERROR  {exc}", file=sys.stderr)

        # ── camera event every 3rd tick ───────────────────────────────────
        if tick % 3 == 0:
            emp, zone, cam = random.choice(assignments)
            action = random.choice(ACTION_TYPES)
            confidence = round(random.uniform(0.82, 0.99), 2)
            try:
                event = post(base, "/camera-events/", {
                    "camera_id": cam["id"],
                    "timestamp": now,
                    "action_type": action,
                    "confidence": confidence,
                    "bounding_box": [100, 80, 220, 200],
                    "video_clip_url": None,
                })
                status = "matched ✓" if event.get("employee_action_id") else "queued (annotation)"
                print(f"  [evt] {action:<12} conf={confidence:.2f}  cam={cam['name']}  → {status}")
            except Exception as exc:
                print(f"  [evt] ERROR  {exc}", file=sys.stderr)

        tick += 1
        print()
        time.sleep(interval)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Live-dashboard simulator")
    parser.add_argument("--url",      default="http://localhost:8000/api", help="Backend API base URL")
    parser.add_argument("--interval", default=1.0, type=float,            help="Seconds between ticks (default: 1)")
    args = parser.parse_args()

    try:
        zones, cameras, employees = seed(args.url)
    except ConnectionError as exc:
        print(f"\nERROR: {exc}\nIs the backend running at {args.url}?", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as exc:
        print(f"\nERROR: Seeding failed — {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        simulate(args.url, zones, cameras, employees, args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
