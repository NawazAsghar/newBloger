from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BlogPost, Profile
from django import forms


class RegistertionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ("title","thumbnail",'slug',"description")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('frist_name', 'last_name', 'email', 'profileImg')
