from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('post/<str:slug>', views.post_details, name='details'),
    path('contact/', views.contact_views, name = 'contact'),
    path('about/', views.about_views, name = 'about'),
    path('register/', views.register_views, name = 'register'),
    path('login/', views.login_views, name = 'login'),
    path('dashboard/', views.dashboard_views, name = 'dashboard'),
    path('logout/', views.logout_views, name = 'logout')
]