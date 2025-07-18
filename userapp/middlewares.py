import logging
import traceback
from django.utils.deprecation import MiddlewareMixin
from django.http import Http404, JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)

class LogRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info(f"[{request.method}] {request.get_full_path()} từ IP {request.META.get('REMOTE_ADDR')}")
        return None

class ExceptionHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        try:
            response = self.get_response(request)
            if response.status_code >= 400:
                try:
                    data = response.data if hasattr(response, 'data') else {}
                except:
                    data = {}
                return JsonResponse({
                    "success": False,
                    "message": data.get("detail", "Something went wrong"),
                    "errors": data,
                    "status": response.status_code
                }, status=response.status_code)

            return response

        except Exception as e:
            import traceback
            if settings.DEBUG:
                traceback.print_exc()
            return JsonResponse({
                "success": False,
                "error": str(e),
                "status": 500
            }, status=500)
