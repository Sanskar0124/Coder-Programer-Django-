from django.shortcuts import render,HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.

# HTML Pages
def home(request):
    # Fetch top three post number of views

    return render(request, 'home/home.html') 

def about(request):
    return render(request, 'home/about.html') 

def contact(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        content = request.POST.get('content')
        print(name, email,phone, content)

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form Correctly")
        else:
            contact = Contact(name=name, email=email,phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, 'home/contact.html') 

def search(request):
    query = request.GET.get('query')
    if len(query) > 80:
        allPosts=Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent =  Post.objects.filter(content__icontains=query)
        allPostsAuthor =  Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)

    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

# Authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        #Get the post parameters
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

    # Chechk for errorneous inputs
        # User name should be under 10 character
        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters")
            return redirect('home')

        #Username should be alphanumeric
        if not username.isalnum():
            messages.error(request, "Username should contain letters and numbers")
            return redirect('home')

        # Passwords should match
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your CoderProgramer account has been succesfully created")
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST.get('loginusername')
        loginpassword = request.POST.get('loginpassword')

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'Succesfully Logged In')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials, Please try again')
            return redirect('home')
        
    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, 'Succesfully Logged Out')
    return redirect('home')