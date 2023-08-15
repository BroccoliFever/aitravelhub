# This is to clear the session data after the user navigates away from the page:
class ClearSessionDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the user navigated away from the URL/search page
        if not request.path.startswith("/search/"):
            request.session.pop("temp_data_list", None)  # Clear session data
        
        return response