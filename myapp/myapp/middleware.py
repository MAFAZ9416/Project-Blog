# Import the necessary modules and classes
from django.urls import reverse
from django.shortcuts import redirect

# Create your middleware here.

#----> Create a middleware to redirect authenticated user to home page if they try to access login and register page
class RedirectAuthenticatedUserMiddleware:

    def __init__(self, get_response):

        # This get_response check we have any next middleware have or not if we have then pass the request to next middleware if not then pass the request
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated :

            path_list = [reverse('login'), reverse('register')]

            # Check if user in the path list or not 
            if request.path in path_list :

                # If user in the path list then redirect to home page
                return redirect(reverse('index'))
        
        response = self.get_response(request)
        return response
    

#----> Create a middleware to restrict unauthenticated user to access the dashboard page and also check if the user have permission to access the dashboard page or not if not then it will show an error message and redirect to the index page
class RestrictUnauthenticatedUserMiddleware:

    def __init__(self, get_response):

        # This get_response check we have any next middleware have or not if we have then pass the request
        self.get_response = get_response

    def __call__(self, request):

        path_list = [reverse('dashboard')]

        if not request.user.is_authenticated and request.path in path_list :
            
            # If user in the path list then redirect to home page
            return redirect(reverse('login'))
         
        response = self.get_response(request)
        return response

            
