"""add worker tracking models

Revision ID: 0001
Revises:
Create Date: 2026-03-26

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "terminals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("map_image_url", sa.String(512), nullable=True),
    )

    op.create_table(
        "zones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("points", sa.JSON(), nullable=False),
        sa.Column("terminal_id", sa.Integer(), sa.ForeignKey("terminals.id"), nullable=False),
    )
    op.create_index("ix_zones_terminal_id", "zones", ["terminal_id"])

    op.create_table(
        "sectors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("points", sa.JSON(), nullable=False),
        sa.Column("zone_id", sa.Integer(), sa.ForeignKey("zones.id"), nullable=False),
    )
    op.create_index("ix_sectors_zone_id", "sectors", ["zone_id"])

    op.create_table(
        "cameras",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("stream_url", sa.String(512), nullable=False),
        sa.Column("terminal_id", sa.Integer(), sa.ForeignKey("terminals.id"), nullable=False),
        sa.Column("zone_id", sa.Integer(), sa.ForeignKey("zones.id"), nullable=True),
        sa.Column("sector_id", sa.Integer(), sa.ForeignKey("sectors.id"), nullable=True),
    )
    op.create_index("ix_cameras_terminal_id", "cameras", ["terminal_id"])
    op.create_index("ix_cameras_zone_id", "cameras", ["zone_id"])

    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("badge_id", sa.String(64), nullable=False, unique=True),
        sa.Column("terminal_id", sa.Integer(), sa.ForeignKey("terminals.id"), nullable=False),
    )
    op.create_index("ix_employees_badge_id", "employees", ["badge_id"])
    op.create_index("ix_employees_terminal_id", "employees", ["terminal_id"])

    # Create camera_events WITHOUT the employee_action_id FK yet (circular dependency)
    op.create_table(
        "camera_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("camera_id", sa.Integer(), sa.ForeignKey("cameras.id"), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("action_type", sa.String(128), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("bounding_box", sa.JSON(), nullable=True),
        sa.Column("video_clip_url", sa.String(512), nullable=True),
        sa.Column("needs_annotation", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("employee_action_id", sa.Integer(), nullable=True),  # FK added after
    )
    op.create_index("ix_camera_events_camera_id", "camera_events", ["camera_id"])
    op.create_index("ix_camera_events_timestamp", "camera_events", ["timestamp"])
    op.create_index("ix_camera_events_needs_annotation", "camera_events", ["needs_annotation"])

    op.create_table(
        "employee_actions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("employee_id", sa.Integer(), sa.ForeignKey("employees.id"), nullable=False),
        sa.Column("zone_id", sa.Integer(), sa.ForeignKey("zones.id"), nullable=True),
        sa.Column("sector_id", sa.Integer(), sa.ForeignKey("sectors.id"), nullable=True),
        sa.Column("action_type", sa.String(128), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("source_event_id", sa.Integer(), sa.ForeignKey("camera_events.id"), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_employee_actions_employee_id", "employee_actions", ["employee_id"])
    op.create_index("ix_employee_actions_timestamp", "employee_actions", ["timestamp"])

    # Now add the deferred FK from camera_events → employee_actions
    op.create_foreign_key(
        "fk_camera_events_employee_action_id",
        "camera_events",
        "employee_actions",
        ["employee_action_id"],
        ["id"],
    )

    op.create_table(
        "sensor_positions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("employee_id", sa.Integer(), sa.ForeignKey("employees.id"), nullable=False),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
        sa.Column("zone_id", sa.Integer(), sa.ForeignKey("zones.id"), nullable=True),
        sa.Column("sector_id", sa.Integer(), sa.ForeignKey("sectors.id"), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_sensor_positions_employee_id", "sensor_positions", ["employee_id"])
    op.create_index("ix_sensor_positions_timestamp", "sensor_positions", ["timestamp"])

    op.create_table(
        "annotations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("camera_event_id", sa.Integer(), sa.ForeignKey("camera_events.id"), nullable=False),
        sa.Column("annotator_id", sa.String(128), nullable=False),
        sa.Column("action_type", sa.String(128), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_annotations_camera_event_id", "annotations", ["camera_event_id"])


def downgrade() -> None:
    op.drop_table("annotations")
    op.drop_table("sensor_positions")
    op.drop_constraint(
        "fk_camera_events_employee_action_id", "camera_events", type_="foreignkey"
    )
    op.drop_table("employee_actions")
    op.drop_table("camera_events")
    op.drop_table("employees")
    op.drop_table("cameras")
    op.drop_table("sectors")
    op.drop_table("zones")
    op.drop_table("terminals")
