"""Pydantic schemas for API request/response."""

from pydantic import BaseModel, Field
from datetime import datetime


class URLCreateRequest(BaseModel):
    """Request model for creating a short URL."""
    long_url: str = Field(..., description="The original long URL to shorten")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "long_url": "https://"
                }
            ]
        }
    }


class URLCreateResponse(BaseModel):
    """Response model for created short URL."""
    short_code: str = Field(..., description="The generated short code")
    short_url: str = Field(..., description="The complete short URL")
    original_url: str = Field(..., description="The original long URL")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "short_code": "aB3xY",
                    "short_url": "http://localhost:8000/aB3xY",
                    "original_url": "https://www.example.com/very/long/url",
                    "created_at": "2025-12-10T10:30:00"
                }
            ]
        }
    }


class URLStatsResponse(BaseModel):
    """Response model for URL statistics."""
    short_code: str = Field(..., description="The short code")
    original_url: str = Field(..., description="The original long URL")
    visit_count: int = Field(..., description="Number of times the short URL was accessed")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "short_code": "aB3xY",
                    "original_url": "https://www.example.com/very/long/url",
                    "visit_count": 42,
                    "created_at": "2025-12-10T10:30:00"
                }
            ]
        }
    }

