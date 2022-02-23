class MyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # number of rows
        # check if response object has a 'content-range' attribute
        if not hasattr(request, 'number_of_rows'):
            response['Content-Range'] = "posts 0-9/319"
        else:
            response['Content-Range'] = f"posts 0-9/{getattr(request, 'number_of_rows')}"

        response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
        return response
