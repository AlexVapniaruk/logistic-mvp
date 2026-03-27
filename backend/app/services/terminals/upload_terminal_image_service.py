import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.terminal import Terminal
from app.schemas.terminal import TerminalReadSchema

UPLOADS_ROOT = Path("/app/uploads")
ALLOWED_TYPES = frozenset({"image/jpeg", "image/png", "image/webp"})


class UploadTerminalImageService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, terminal_id: int, file: UploadFile) -> TerminalReadSchema:
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=422, detail="Only jpg, png, webp accepted")

        result = await self.db.execute(select(Terminal).where(Terminal.id == terminal_id))
        terminal = result.scalar_one_or_none()
        if terminal is None:
            raise HTTPException(status_code=404, detail="Terminal not found")

        self._delete_old_file(terminal.map_image_url)

        ext = "jpg" if file.content_type == "image/jpeg" else file.content_type.split("/")[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        dest_dir = UPLOADS_ROOT / "terminals" / str(terminal_id)
        dest_dir.mkdir(parents=True, exist_ok=True)
        (dest_dir / filename).write_bytes(await file.read())

        terminal.map_image_url = f"/uploads/terminals/{terminal_id}/{filename}"
        await self.db.commit()
        await self.db.refresh(terminal)
        return TerminalReadSchema.model_validate(terminal)

    def _delete_old_file(self, current_url: str | None) -> None:
        if not current_url or not current_url.startswith("/uploads/"):
            return
        old_path = UPLOADS_ROOT / current_url.removeprefix("/uploads/").lstrip("/")
        if old_path.exists():
            old_path.unlink()
