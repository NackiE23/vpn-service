from django.shortcuts import redirect
from django.urls import resolve


class CheckUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        referer = request.META.get('HTTP_REFERER', None)
        if referer and not request.path.startswith(("/media/", "/static/")):
            path = request.path
            try:
                resolve(path)
            except Exception:
                # Not resolved path
                new_url = f"{referer}{path}?{'&'.join([f'{key}={value}' for key, value in request.GET.items()])}"
                return redirect(new_url)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
