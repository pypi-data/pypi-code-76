HEADERS = {
    "X-FRAME-Options": "DENY",
    "Content-Security-Policy": "frame-ancestors 'none'",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Cache-Control": "no-cache, no-store",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection": "1; mode=block",
}


class SecurityHeaderMiddleware(object):
    """
    Add security headers to all responses
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        for k, v in HEADERS.items():
            response[k] = v

        return response
