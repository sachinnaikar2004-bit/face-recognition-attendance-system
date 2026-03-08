"""
Logging middleware for request/response logging.
"""

import time
import logging
from datetime import datetime
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        """Process request and log details."""
        # Add timestamp to request state
        request.state.timestamp = datetime.utcnow()
        
        # Start timer
        start_time = time.time()
        
        # Log request
        await self._log_request(request)
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        await self._log_response(request, response, process_time)
        
        # Add processing time to response headers
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
    
    async def _log_request(self, request: Request):
        """Log incoming request details."""
        try:
            client_ip = self._get_client_ip(request)
            
            logger.info(
                f"Request: {request.method} {request.url.path} "
                f"from {client_ip} at {request.state.timestamp}"
            )
            
        except Exception as e:
            logger.error(f"Error logging request: {str(e)}")
    
    async def _log_response(self, request: Request, response: Response, process_time: float):
        """Log response details."""
        try:
            client_ip = self._get_client_ip(request)
            
            logger.info(
                f"Response: {response.status_code} for {request.method} {request.url.path} "
                f"from {client_ip} in {process_time:.4f}s"
            )
            
        except Exception as e:
            logger.error(f"Error logging response: {str(e)}")
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request."""
        # Check for forwarded IP
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check for real IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Return client host
        return request.client.host if request.client else "unknown"


def setup_logging(app):
    """Setup logging middleware for the application."""
    app.add_middleware(LoggingMiddleware)
