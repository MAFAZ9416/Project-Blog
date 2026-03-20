#----> Import the necessary modules 
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Categorys, Post


#----> Create your forms here.

#----> Create a Contact form
class ContactForm(forms.Form):
    name = forms.CharField(label = 'Name', max_length = 100, required = True)
    email = forms.EmailField(label = 'Email', required = True)
    message = forms.CharField(label = 'Message', required = True)


#----> Create a Register form
class RegisterForm(forms.ModelForm):
    username = forms.CharField(label = 'User_Name', max_length = 100, required = True)
    email = forms.EmailField(label = 'Email', max_length = 100, required = True)
    password = forms.CharField(label = 'Password',  max_length = 100, required = True)
    password_confirm = forms.CharField(label = 'Confirm Password',  max_length = 100, required = True)

    class Meta :
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Check if password and confirm password is match or not
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password and Confirm Password do not match")


#----> Create a login form        
class LoginForm(forms.Form):

    username = forms.CharField(label = 'User_Name', max_length = 100, required = True)
    password = forms.CharField(label = 'Password',  max_length = 100, required = True)

    def clean(self):

        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Check the user and password is valid or not
        if username and password:
            user = authenticate(username = username, password = password)
            if user is None:
                raise forms.ValidationError("Invalid username and password")


#----> Create a ForgotPassword form 
class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(label = 'Email', max_length = 200, required = True)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if the email is associated with any user account or not
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user is associated with this email address")

        return email


#----> Create a ResetPassword form 
class ResetPasswordForm(forms.Form):

    new_password = forms.CharField(label = 'New Password', min_length = 8)
    confirm_password = forms.CharField(label = 'Confirm Password', min_length = 8)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New Password and Confirm Password do not match")


 #----> Create a Post form and use this form to update the post in the database    
class PostForm(forms.ModelForm):

    title = forms.CharField(label = 'Title', max_length = 200, required = True)
    content = forms.CharField(label = 'Content', required = True)
    category = forms.ModelChoiceField(label = 'Category', required = True, queryset = Categorys.objects.all())
    img_url = forms.ImageField(label = 'image', required = False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'img_url']

    def clean(self):

        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        # Check if the title and content is has valid characters or not 
        if title and len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        
        if content and len(content) < 10 :
            raise forms.ValidationError("content must be at least 10 characters long.")
    
    def save(self, commit = ...):

        cleaned_data = super().clean()
        image = cleaned_data.get('img_url')
        
        post = super().save()

        # check if image filed have or not
        if not image :
            img_url = "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?_=20200913095930"
            post.img_url = img_url 

        else :
            post.img_url = image

        if commit:
            post.save()
        
        return post