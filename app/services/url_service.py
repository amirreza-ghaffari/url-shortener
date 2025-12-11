"""URL shortener service layer containing business logic."""

from fastapi import HTTPException, status
from sqlmodel import select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.models import ShortURL
from app.services.encoder_service import EncoderService


class URLService:
    """Service class for URL shortening operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_short_url_object(self, original_url: str) -> ShortURL:

        statement = select(ShortURL).where(ShortURL.original_url == original_url)
        result = await self.session.execute(statement)
        existing_url = result.scalar_one_or_none()

        if existing_url:
            return existing_url

        uuid7 = EncoderService.generate_uuid7()
        short_code = EncoderService.uuid_to_base62(uuid7)

        new_url = ShortURL(
            id=uuid7,
            original_url=original_url,
            short_code=short_code
        )
        self.session.add(new_url)
        await self.session.commit()
        await self.session.refresh(new_url)
        return new_url

    async def get_url_by_short_code(self, short_code: str) -> ShortURL:

        try:
            uuid_id = EncoderService.base62_to_uuid(short_code)
        except (ValueError, IndexError):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid short code '{short_code}'"
            )

        url_entry = await self.session.get(ShortURL, uuid_id)

        if not url_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Short URL with code '{short_code}' not found"
            )

        return url_entry

    async def redirect_and_track(self, short_code: str) -> ShortURL:

        url_entry = await self.get_url_by_short_code(short_code)

        statement = (
            update(ShortURL)
            .where(ShortURL.id == url_entry.id)
            .values(visit_count=ShortURL.__table__.c.visit_count + 1)
        )
        await self.session.execute(statement)
        await self.session.commit()

        return url_entry

