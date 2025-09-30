# bookings/middleware.py
import logging
import time
import json

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Logs request start, method, path, body (if small), response status and duration.
    Place this middleware after common Django middleware as configured in settings.py.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        try:
            # basic request info
            method = request.method
            path = request.get_full_path()
            # try to capture small JSON bodies safely
            body = None
            try:
                if method in ("POST", "PUT", "PATCH") and request.body:
                    raw = request.body.decode("utf-8")[:2000]
                    body = raw
            except Exception:
                body = "<could not decode>"

            logger.info(f"Request start: {method} {path} body={body}")

            response = self.get_response(request)

            duration = time.time() - start
            logger.info(f"Request finished: {method} {path} status={response.status_code} time={duration:.3f}s")
            return response
        except Exception as ex:
            # log exception details
            logger.exception(f"Unhandled exception during request: {ex}")
            raise
