from fastapi import (
    APIRouter,
    Request,
    Depends,
    status,
)
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.api.schemas import (
    URLCreateRequest,
    URLCreateResponse,
    URLStatsResponse,
)
from app.services.url_service import URLService

router = APIRouter()


@router.post("/shorten", response_model=URLCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    url_request: URLCreateRequest,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a short URL from a long URL.
    Returns the generated short code and complete short URL.
    """

    url_service = URLService(session)
    url_entry = await url_service.create_short_url_object(url_request.long_url)

    base_url = str(request.base_url).rstrip('/')
    short_url = f"{base_url}/{url_entry.short_code}"

    return URLCreateResponse(
        short_code=url_entry.short_code,
        short_url=short_url,
        original_url=url_entry.original_url,
        created_at=url_entry.created_at
    )

@router.get("/{short_code}", response_class=RedirectResponse)
async def redirect_to_url(
    short_code: str,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    """
    Redirect to the original URL using the short code.
    Also increments the visit counter for statistics.
    """

    url_service = URLService(session)
    url_entry = await url_service.redirect_and_track(short_code)

    return RedirectResponse(
        url=url_entry.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )


@router.get("/stats/{short_code}", response_model=URLStatsResponse)
async def get_url_stats(
    short_code: str,
    session: AsyncSession = Depends(get_session)
):
    """
    Get statistics for a short URL.
    Returns visit count and other metadata.
    """

    url_service = URLService(session)
    url_entry = await url_service.get_url_by_short_code(short_code)

    return URLStatsResponse(
        short_code=url_entry.short_code,
        original_url=url_entry.original_url,
        visit_count=url_entry.visit_count,
        created_at=url_entry.created_at
    )
