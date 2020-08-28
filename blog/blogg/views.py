from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Contact,Blog,BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from blogg.templatetags import get_val

#HTML Pages
def home(request):
    # fetch data for most 3 popular blogs

    blog = Blog.objects.all().order_by('-views')[0:3]

    return render(request,"home.html",{'blog':blog})

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please fill the form correctly")
        else:
            contact = Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Your Form Filled Submitted")
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def blogpost(request):
    posts = Blog.objects.all()
    return render(request,"blogpost.html",{'posts':posts})

def blog(request,slug):
    post=Blog.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)

    replydict= {}
    for reply in replies:
        if reply.parent.sno not in replydict.keys():
            replydict[reply.parent.sno]=[reply]
        else:
            replydict[reply.parent.sno].append(reply)

    return render(request,'blog.html',{'post':post,'comments':comments,'user':request.user,'replydict':replydict})

def search(request):
    query=request.GET['query']
    if len(query)>78:
        posts=Blog.objects.none()
    else:
        poststitle=Blog.objects.filter(title__icontains=query)
        postcontent=Blog.objects.filter(content__icontains=query)
        posts=poststitle.union(postcontent)
    if posts.count()  == 0:
        messages.warning(request,"No search result found.Please refine your query")

    return render(request,"search.html",{'posts':posts,'query':query})

#Authenticated API -which redirect or return error
def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

    # check for errorenous
        if not username.isalnum():
            messages.error(request, "Username should contain letters and numbers")
            return redirect("home")

        if len(username)>10:
            messages.error(request,"Username must be under 10 characters")
            return redirect("home")
        if pass1 != pass2:
            messages.error(request, "Password should be same")
            return redirect("home")

    # create the user
        myuser=User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"your account created successfully")
        return redirect('home')

    else:

        return HttpResponse('404 Not Found')

def handlelogin(request):
    if request.method=="POST":
        lusername=request.POST['lusername']
        lpassword=request.POST['lpassword']
        user=authenticate(username=lusername,password= lpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"successfully login")
            return redirect('home')
        else:
            messages.error(request,"invalid credentials.Please try again")
            return redirect('home')
    else:
        return HttpResponse('404:Not found')

def handlelogout(request):
    logout(request)
    messages.success(request, "successfully logout")
    return redirect('home')

def postcomment(request):
    if request.method=="POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get("postSno")
        post=Blog.objects.get(sno=postSno)
        parentSno=request.POST.get("parentSno")
        if parentSno == " ":
            comment=BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,"Your comment posted successfully")
        else:
            parent=BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post,parent=parent)
            comment.save()
            messages.success(request, "Your reply posted successfully")

    return redirect(f'/blog/{post.slug}')




