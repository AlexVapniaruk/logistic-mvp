import os
from pathlib import Path


class RunInferenceService:
    """Wraps the YOLO model for a single-frame inference call."""

    def __init__(self, model_path: str | None = None) -> None:
        self._model_path = model_path or os.getenv("MODEL_PATH", "ml_models/best.pt")
        self._model = None  # lazy-loaded on first call

    async def execute(self, frame_bytes: bytes) -> list[dict]:
        model = self._load_model()
        results = model(frame_bytes)
        return self._parse_results(results)

    def _load_model(self):
        if self._model is None:
            from ultralytics import YOLO  # imported lazily to keep startup fast
            self._model = YOLO(self._model_path)
        return self._model

    def _parse_results(self, results) -> list[dict]:
        detections = []
        for result in results:
            for box in result.boxes:
                detections.append({
                    "class_name": result.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy[0].tolist(),
                })
        return detections
