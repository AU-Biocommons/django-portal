"""View-related utilities."""

import logging
import traceback
from django.http import JsonResponse
from functools import wraps

logger = logging.getLogger('django')


def api_view(methods):
    """A decorator for API endpoints.
    
    Accepts an optional list of methods to allow. Catches errors and returns
    an appropriate JSONResponse.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if methods and request.method not in methods:
                return JsonResponse({
                    'error': 'HTTP method not allowed'
                }, status=405)
            try:
                return func(request, *args, **kwargs)
            except Exception as e:
                logger.error(traceback.format_exc())
                return JsonResponse({
                    'error': str(e)
                }, status=500)
        return wrapper
    return decorator
