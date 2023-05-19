from django.contrib import admin
from .models import BlogPost, Profile

@admin.register(BlogPost)
class AdminBlogPost(admin.ModelAdmin):
    list_display = ['title', 'auther', 'created_date']
    
@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ['user','frist_name', 'last_name', 'email']
