from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
from datetime import datetime

# Use a custom logger instead of uvicorn.access to avoid format conflicts
logger = logging.getLogger("url_shortener")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all incoming requests and responses."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_ip = request.client.host if request.client else 'unknown'

        logger.info(
            f"[{timestamp}] IP: {client_ip} - "
            f"Incoming request: {request.method} {request.url.path}"
        )

        response = await call_next(request)

        logger.info(
            f"[{timestamp}] IP: {client_ip} - "
            f"Response: {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Duration: {time.time() - start_time:.4f}s"
        )

        return response


def add_logging_middleware(app):
    app.add_middleware(LoggingMiddleware)
