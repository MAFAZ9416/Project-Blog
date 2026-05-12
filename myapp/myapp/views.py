#-----> Import neccessary modules 
from django.shortcuts import render


#----> Create custom 404 page views
def custom_404_views(request, exception):
    return render(request, '404.html', status=404)