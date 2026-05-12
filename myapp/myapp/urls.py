"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#-----> Import neccessary modules 
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

# handle custom 404 page
handeler404 = 'myapp.views.custom_404_views'

#----> Main domain url
urlpatterns = [
    path('blog/', include('blog.urls')),
    path('blog/admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)# static method to show the local image to deploy the server and display into the online
