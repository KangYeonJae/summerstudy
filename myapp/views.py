from django.shortcuts import render,get_object_or_404,redirect
from .forms import MyappForm, CommentForm
from .models import Myapp
from django.utils import timezone
from .forms import SigninForm, SignupForm 
from django.urls.base import reverse
from django.contrib.auth.models import User 
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout 


# Create your views here.

def post(request):
    if request.method =='POST':
        form=MyappForm(request.POST)
        if form.is_valid():
            myapp=form.save(commit=False)
            myapp.update_date=timezone.now()
            myapp.save()
            return redirect('show')
    
    else:
        form=MyappForm()
        return render(request, 'post.html',{'form':form})

def show(request):

    myapps=Myapp.objects.order_by('-id')
    return render(request, 'show.html', {'myapps':myapps})


def detail(request, myapp_id):
    myapp_detail =get_object_or_404(Myapp, pk=myapp_id)
    if request.method=="POST":
        comment_form=CommentForm(request.POST)
        comment_form.instance.myapp_id=myapp_id
        if comment_form.is_valid():
            comment=comment_form.save()
    
    comment_form=CommentForm()
    comments=myapp_detail.comments.all()
    return render(request, 'detail.html', {'myapp':myapp_detail,'comments':comments,'comment_form':comment_form})

def edit(request, pk):
    myapp=get_object_or_404(Myapp,pk=pk)
    if request.method =='POST':
        form=MyappForm(request.POST, instance=myapp)
        if form.is_valid():
            myapp=form.save(commit=False)
            myapp.update_date=timezone.now()
            myapp.save()
            return redirect('show')
    else:
        form=MyappForm(instance=myapp)
        return render(request,'edit.html',{'form':form})

def delete(request,pk):
    myapp=Myapp.objects.get(id=pk)
    myapp.delete()
    return redirect('show')

#회원가입
def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html', {'form':SignupForm()} )
    
    
    elif request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password']  == form.cleaned_data['password_check']:

                new_user = User.objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password'])

                new_user.last_name = form.cleaned_data['last_name']
                new_user.first_name = form.cleaned_data['first_name']

                new_user.save()
                
                return redirect('show')      
            else:
                return render(request, 'signup.html',{'form':form, 'error':'비밀번호와 비밀번호 확인이 다릅니다.'})

        else: 
            return render(request, 'signup.html',{'form':form})
        
#로그인
def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {'form':SigninForm()} )
    
    elif request.method == "POST":
        form = SigninForm(request.POST)
        id = request.POST.get('username')
        pw = request.POST.get('password')
        u = authenticate(username=id, password=pw)

        if u: 
            login(request, user=u) 
            return redirect('show')
        else:
            return render(request, 'signin.html',{'form':form, 'error':'아이디나 비밀번호가 일치하지 않습니다.'})
    

#로그아웃
def signout(request): 
    logout(request) 
    return redirect('show')
