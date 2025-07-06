from django.shortcuts import render,redirect
from django.http import HttpResponse
from book.models import *
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def blog(request):
   context={'page': "ADD BLOG"}
   if request.method=="POST":
      blog_name=request.POST.get('blog_name')
      blog_info=request.POST.get('blog_info')
      blog_date=request.POST.get('blog_date')
      blog_image=request.FILES.get('blog_image')

      Blog.objects.create(
         blog_name=blog_name,
         blog_info=blog_info,
         blog_date=blog_date,
         blog_image=blog_image
      )
      return redirect('/blogs/')
   
   
   return render(request,"mani/home.html",context)

@login_required(login_url="/login/")
def blog_page(request):
    blog_posts = Blog.objects.all()
    context = {
        'page': "blog_page",
        'blog': blog_posts  # Make sure 'blog' is passed as context
    }
    queryset=Blog.objects.all()
    if request.GET.get('search'):
       queryset=queryset.filter(blog_name__icontains=request.GET.get('search'))
    context={'blog':queryset}
   
    
    return render(request, "mani/blog_page.html", context)

def register(request):
   context={'page':"Register Page"}
   if request.method=="POST":
       first_name=request.POST.get('first_name')
       last_name=request.POST.get('last_name')
       username=request.POST.get('user_name')
       password=request.POST.get('password')

       user=User.objects.filter(username=username)
       if user.exists():
          messages.info(request,'username already exists')
          return redirect('/register/')
       
       user=User.objects.create_user(
          first_name=first_name,
          last_name=last_name,
          username=username
       )
       user.set_password(password)
       user.save()
       messages.success(request,"Account successfully created")
       return redirect('/login/')
   
   return render(request,"mani/register.html",context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request,'Invalid username')

        user = authenticate(username=username, password=password)  # ✅ Handles both username & password

        if user is None:
            messages.error(request, 'Invalid password')  # ✅ Clearer message
            return redirect('/login/')  
        else:
            login(request, user)
            return redirect('/blogs/')  # ✅ Redirect to blogs after login

    context = {'page': "LOGIN PAGE"}
    return render(request, "mani/login.html", context)

@login_required(login_url="/login/")
def delete(request,id):
    queryset=Blog.objects.get(id=id)
    queryset.delete()
    return redirect('/blogs')
def logout_page(request):
   logout(request)
   return redirect('/login/')