from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('post/<str:slug>', views.post_details, name='details'),
    path('contact/', views.contact_views, name = 'contact'),
    path('about/', views.about_views, name = 'about')
]