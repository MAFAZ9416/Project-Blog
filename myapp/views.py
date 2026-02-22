from django.shortcuts import render

def custom_404_views(request, exception):
    return render(request, '404.html', status=404)