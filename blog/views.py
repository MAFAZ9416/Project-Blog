from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404
import logging
from .models import Post, About
from django.core.paginator import Paginator
from .forms import ContactForm, LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# variables 

titles = ["Latest Posts","Post Details","Post Titles"]

# --> Static Data for testing purpose
# posts_details = [
#     {"post_id" : 1, "title" : "post 1", "content" : "This is the content of post 1."},
#     {"post_id" : 2, "title" : "post 2", "content" : "This is the content of post 2."},
#     {"post_id" : 3, "title" : "post 3", "content" : "This is the content of post 3."},
#     {"post_id" : 4, "title" : "post 4", "content" : "This is the content of post 4."},
#     {"post_id" : 5, "title" : "post 5", "content" : "This is the content of post 5."}
# ]

# Create your views here.

def index(request):
    # Data's From DataBase Connection
    all_posts = Post.objects.all()

    # pagination
    paginator = Paginator(all_posts, 5) # Show 5 posts per page
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)

    return render(request, 'index.html',{"blog_title" : titles[0], "page_objs" : page_obj})

def post_details(request, slug):
    # Static Data for testing purpose
    # post = next((values for values in posts if values['title'] == post_id), None)

    try:
    # Data's From DataBase Connection
        post = Post.objects.get(slug=slug)
        related_post = Post.objects.filter(category = post.category).exclude(pk = post.id)
        return render(request, 'details.html',{"post_title" : titles[1], "post": post, "related_posts":related_post})
    
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

def contact_views(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        logger = logging.getLogger('TESTLOGGER')

        if form.is_valid():         
            logger.debug(f'Contact form name is {form.cleaned_data["name"]} and email is {form.cleaned_data["email"]} and message is {form.cleaned_data["message"]}')
            return render(request, 'contact.html', {'forms' : form, 'success_msg' : 'Your message has been sent successfully!'})
        
        else:
            logger.debug('Contact form is not valid')
        return render(request, 'contact.html', {'forms' : form})

    return render(request, 'contact.html')

def about_views(request):

    # connect to database and admin panel to add about content
    about_content = About.objects.first()

    if about_content is None or not about_content.content :
        about_content = "No content available on about page..."
    else:
        about_content = about_content.content

    return render(request, 'about.html', {'about_content': about_content})

def register_views(request):

    form = RegisterForm()

    if request.method == 'POST' :
        form = RegisterForm(request.POST)

        if form.is_valid() :
            user = form.save(commit=False) # this will create a user object but not save it to the database yet
            user.set_password(form.cleaned_data['password']) # hash the password
            user.save()# save data to database 
            print('User Registered Successfully!')

            # success message
            messages.success(request, 'User Registered Successfully!, now you can login to your account.')

            # redirect to the login page
            return redirect('login')

    return render(request, 'register.html', {'form' : form})

def login_views(request):
    form = LoginForm()

    if request.method == 'POST' :
        form = LoginForm(request.POST)

        if form.is_valid() :

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)

            if user is not None:
                auth_login(request, user)
                print('User Login Successfully!')
                return redirect('dashboard') # redirect to the Dashboard

    return render(request, 'login.html', {'form' : form})

def dashboard_views(request):

    blog_title = 'My Post'
    return render(request, 'dashboard.html', {'blog_title' : blog_title})

def logout_views(request):
    auth_logout(request)
    return redirect('index')