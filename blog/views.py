#----> Import the necessary modules
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse,Http404
import logging
from .models import Post, About, Categorys
from django.core.paginator import Paginator
from .forms import ContactForm, LoginForm, PostForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts  import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, permission_required

# variables 

titles = ["Latest Posts","Post Details","Post Titles"]


#-----> Create your views here.

#----> Create a Index view to display the all post in home page
def index(request):

    # Data's From DataBase Connection
    all_posts = Post.objects.filter(is_published = True)

    # pagination
    paginator = Paginator(all_posts, 5) # Show 5 posts per page
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)

    return render(request, 'index.html',{"blog_title" : titles[0], "page_objs" : page_obj})


#----> Create a Post Details view to display the details of the post when we click on the post details in index page
def post_details(request, slug):
    
    # Check the user have permission to view the detail page
    if request.user and not request.user.has_perm('blog.view_post'):
        messages.error(request, "Sorry you are not have a permission to view Detail page !")
        return redirect('index')

    # we use try and exception to handle the error's
    try:

    # Data's From DataBase Connection
        post = Post.objects.get(slug=slug)
        related_post = Post.objects.filter(category = post.category).exclude(pk = post.id)
        return render(request, 'details.html',{"post_title" : titles[1], "post": post, "related_posts":related_post})
    
    # if the post is not exist in the database then it will raise a 404 error and show the message "Post does not exist"
    except Post.DoesNotExist:
        raise Http404("Post does not exist")


# ---> Check the user is authenticated or not, if not then redirect to login page
@login_required
# Create a contact view to display the contact page and handle the contact form submission
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


# ---> Check the user is authenticated or not, if not then redirect to login page
@login_required
# Create an about view to display the about page details
def about_views(request):

    # connect to database and admin panel to add about content
    about_content = About.objects.first()

    if about_content is None or not about_content.content :
        about_content = "No content available on about page..."
    else:
        about_content = about_content.content

    return render(request, 'about.html', {'about_content': about_content})


#----> Create a register view to display the register page and handle the register form submission and redirect to the login page after successful registration
def register_views(request):

    form = RegisterForm()

    if request.method == 'POST' :
        form = RegisterForm(request.POST)

        if form.is_valid() :
            user = form.save(commit=False) # this will create a user object but not save it to the database yet
            user.set_password(form.cleaned_data['password']) # hash the password
            user.save()# save data to database 
            
            # Add user to default(reader) group
            reader_group, created = Group.objects.get_or_create(name = 'Readers')
            user.groups.add(reader_group)

            # success message
            messages.success(request, 'User Registered Successfully!, now you can login to your account.')

            # redirect to the login page
            return redirect('login')

    return render(request, 'register.html', {'form' : form})


#----> Create a login view to display the login page and handle the login verification and redirect to the dashboard page after successful login
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
                return redirect('dashboard') # redirect to the Dashboard

    return render(request, 'login.html', {'form' : form})


#----> Create a dashboard view to display the dashboard page and handle the post creation, post editing, post deletion and post publishing and also display the all user post of the logged in user in the dashboard page
def dashboard_views(request):

    blog_title = 'My Post'

    # Getting post's
    all_posts = Post.objects.filter(user = request.user)

    # pagination
    paginator = Paginator(all_posts, 5) # Show 5 posts per page
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)

    return render(request, 'dashboard.html', {'blog_title' : blog_title, 'page_objs' : page_obj})


# ---> Check the user is authenticated or not, if not then redirect to login page
@login_required
# Create a logout view to handle the user logout and redirect to the index page after successful logout
def logout_views(request):
    auth_logout(request)
    return redirect('index')


# ---> Check the user is authenticated or not, if not then redirect to login page
@login_required
# Create a forgot password view to display the forgot password page and handle the forgot password form submission and send the reset password email to the user email address
def forgot_password_views(request):

    form = ForgotPasswordForm()

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            site = get_current_site(request)
            domain = site.domain

            subject = 'Password Reset Request'

            message = render_to_string('reset_password_Email.html', {
                'domain': domain,
                'uid': uid,
                'token': token
            })

            send_mail(subject, message, 'noreply@jvlcode.com', [email])

            messages.success(request, 'Email sent successfully! Check your inbox.')

    return render(request, 'forgot_password.html', {'form': form})


# ---> Check the user is authenticated or not, if not then redirect to login page
@login_required
# Create a reset password view to display the reset password page and handle the reset password form submission and reset the user password and set the new password then redirect to the login page after successful password reset
def reset_password_views(request, uidb64, token):
    form = ResetPasswordForm()

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            
            if user and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'password reset successfully! You can now login with your new password.')
                return redirect('login') 
            
            else:
                messages.error(request, 'The reset password link is invalid or has expired.')

    return render(request, 'reset_password.html', {'form': form})


# ---> Check the user is authenticated or not, if not then redirect to login page and also check the user have permission to add post or not if not then it will show an error message and redirect to the index page
@login_required
@permission_required('blog.add_post', raise_exception=True)
# Create a new post view to display the new post page and handle the new post form submission and create a new post and redirect to the dashboard page after successful post creation
def new_post_views(request):
    form = PostForm()
    categorys = Categorys.objects.all()

    #forms 
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit = False)
        post.user = request.user
        post.save()
        return redirect('dashboard')

    return render(request, 'new_post.html', {'categorys' : categorys, 'form' : form})


# ---> Check the user is authenticated or not, if not then redirect to login page and also check the user have permission to change post or not if not then it will show an error message and redirect to the index page
@login_required
@permission_required('blog.change_post', raise_exception=True)
# Create an edit post view to display the edit post page and handle the edit post form submission and update the post and redirect to the dashboard page after successful post update
def edit_post_views(request, post_id):
    categorys = Categorys.objects.all()
    post = get_object_or_404(Post, id=post_id)
    form = PostForm()

    # form
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post Updated Successfully !")
            return redirect('dashboard')

    return render(request, 'edit_post.html', {'categorys' : categorys, 'form' : form, 'post' : post})


# ---> Check the user is authenticated or not, if not then redirect to login page and also check the user have permission to delete post or not if not then it will show an error message and redirect to the index page
@login_required
@permission_required('blog.delete_post', raise_exception=True)
# Create a delete post view to handle the post deletion and redirect to the dashboard page after successful post deletion
def delete_post_views(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "Post Deleted Successfully !")
    return redirect('dashboard')


# ---> Check the user is authenticated or not, if not then redirect to login page and also check the user have permission to publish post or not if not then it will show an error message and redirect to the index page
@login_required
@permission_required('blog.is_published', raise_exception=True)
# Create a publish post view to handle the post publishing and redirect to the dashboard page after successful post publishing
def is_published_views(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    post.is_published = True
    post.save()
    messages.success(request, "Post Published Successfully !")
    return redirect('dashboard')
