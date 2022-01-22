class MyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # number of rows
        response['Content-Range'] = 10
        response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
        return response
