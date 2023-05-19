from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core import validators
from django import forms

def desc_vali(value):
    if len(value) <= 150:
        raise forms.ValidationError("Your description is too short.")

class BlogPost(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    thumbnail = models.ImageField(upload_to='thumbnail', null=True, blank=True)
    title = models.CharField(max_length=500)
    description = RichTextField(blank=True, validators=[desc_vali])
    auther = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileImg = models.ImageField(upload_to='profiles')
    frist_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)