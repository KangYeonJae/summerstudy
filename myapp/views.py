from django.shortcuts import render,get_object_or_404,redirect
from .forms import MyappForm
from .models import Myapp
from django.utils import timezone

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
    return render(request, 'detail.html', {'myapp':myapp_detail})

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