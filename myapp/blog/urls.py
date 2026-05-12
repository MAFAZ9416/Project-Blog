#----> Import the necessary modules
from django.urls import path
from . import views


#----> Create a url path for each view function in the views.py file 
urlpatterns = [
    path('', views.index, name = 'index'),
    path('post/<str:slug>', views.post_details, name='details'),
    path('contact/', views.contact_views, name = 'contact'),
    path('about/', views.about_views, name = 'about'),
    path('register/', views.register_views, name = 'register'),
    path('login/', views.login_views, name = 'login'),
    path('dashboard/', views.dashboard_views, name = 'dashboard'),
    path('logout/', views.logout_views, name = 'logout'),
    path('forgot_password/', views.forgot_password_views, name = 'forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password_views, name = 'reset_password'),
    path('new_post/', views.new_post_views, name = 'new_post'),
    path('edit_post/<int:post_id>', views.edit_post_views, name = 'edit_post'),
    path('delete_post/<int:post_id>', views.delete_post_views, name = 'delete_post'),
    path('is_published/<int:post_id>', views.is_published_views, name = 'is_published'),
]