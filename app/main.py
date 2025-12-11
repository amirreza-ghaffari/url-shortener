from fastapi import FastAPI
from app.api import endpoints
from app.middleware.logging import add_logging_middleware

app = FastAPI(
    title="URL Shortener API",
    description="A simple URL shortener service similar to bit.ly",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(endpoints.router)

add_logging_middleware(app)
