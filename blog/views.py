from django.contrib.auth.models import User
from django.contrib.messages.api import error
from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import BlogPost, Profile
from .forms import RegistertionForm, BlogPostForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    all_blogs = BlogPost.objects.all().order_by('created_date')
    paginator = Paginator(all_blogs, 6)
    page_num = request.GET.get('page')
    blogs = paginator.get_page(page_num)
    params = {'blogs': blogs, 'home':'active'}
    return render(request, 'home.html', params)
    
def about(request):
    params = {'about':'active'}
    return render(request, 'about.html', params)
    
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request = request, data = request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username = uname, password = upass)
            if user  is not None:
                login(request, user)
                messages.success(request, 'You logged-in successfully!')
                return HttpResponseRedirect('/dashboard/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form, 'login':'active'})

def user_signup(request):
    if request.method == 'POST':
        form = RegistertionForm(request.POST)
        if form.is_valid():
            newUser = form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            newUser = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, newUser)
            return HttpResponseRedirect('/createProfile/')
    else: 
        form = RegistertionForm()
    return render(request, 'signup.html', {'form':form, 'signup':'active'})

def profile_form(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        profile_user = User.objects.get(pk=request.user.id)
        if form.is_valid():
            frist_name = form.cleaned_data['frist_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            profileImg = form.cleaned_data['profileImg']
            user = profile_user
            data = Profile(frist_name=frist_name, last_name=last_name, email=email, profileImg=profileImg, user=user)
            data.save()
            return HttpResponseRedirect('/dashboard/')
    form = ProfileForm()
    params = {"profile":'active', "form":form}
    return render(request, 'profile_form.html', params)

@login_required
def changeProfile(request):
    profile = Profile.objects.get(user = request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,  request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profileView/')
    params = {"form":form}
    return render(request, 'profileChange.html', params)

@login_required
def profileView(request):
    try:
        profile_data = Profile.objects.get(user = request.user)
        user_posts = BlogPost.objects.filter(auther = request.user)
        allPosts = len(user_posts)
        params = {"data":profile_data, "allPosts":allPosts}
        return render(request, 'profileView.html', params)
    except:
        return HttpResponseRedirect("/createProfile/")

@login_required
def changePass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "YOUR password changed successfly")
            return HttpResponseRedirect("/dashboard/")
        else:
            messages.warning(request, "YOUR password is week OR You din't enter it!")
            return HttpResponseRedirect('/changePass/')
    else:
        form = PasswordChangeForm(user = request.user)
        return render(request, 'changePass.html', {'form':form})

@login_required
def dashboard(request):
    userblog = BlogPost.objects.filter(auther = request.user)
    return render(request, 'dishbord.html', {"blogs":userblog, 'dashboard':'active'})

def blogview(request, slug):
    blog = BlogPost.objects.filter(slug = slug).first()
    auther = False
    if str(request.user) == str(blog.auther):
        auther = True
    return render(request, 'blogview.html', {'blog': blog, "auther":auther})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login/")

@login_required
def editeblog(request, slug):
    blog = BlogPost.objects.filter(slug = slug).first()
    if request.method == 'POST':
        form = BlogPostForm(request.POST,request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Your post has been edited successfully.")
            return redirect('blogview', slug=blog.slug)
    else:
        form = BlogPostForm(instance=blog)
    return render(request, 'editeBlog.html', {'form':form})

@login_required
def deletePost(request, slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            blog = BlogPost.objects.filter(slug = slug)
            blog.delete()
            messages.info(request, "Your post added successfully.")
            return HttpResponseRedirect('/dashboard/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login/')

@login_required
def addblog(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST,  request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            thumbnail = form.cleaned_data['thumbnail']
            disc = form.cleaned_data['description']
            slug = form.cleaned_data['slug']
            auther = request.user
            post = BlogPost(title=title, thumbnail=thumbnail, slug=slug, description=disc, auther=auther)
            post.save()
            messages.success(request, "Your post added successfully.")
            return HttpResponseRedirect('/dashboard/')
    else:
        form = BlogPostForm()
    return render(request, 'addBlog.html', {'form':form})


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)