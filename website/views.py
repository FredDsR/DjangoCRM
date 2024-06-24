from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,
                            username=username,
                            password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "There was an error loggin in. Please, try again.")
            return redirect('home')
    else:
        records = Record.objects.all()
        return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def register_user(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)
            login(request, user)

            messages.success(request, "You have successfully been signed up!")
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record': record})
    
    messages.error(request, 'Access denied.')
    return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Record deleted successfully!')
    
    messages.error(request, 'Access denied.')
    return redirect('home')

def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record added successfully!')
                return redirect('home')

        return render(request, 'add_record.html', {'form': form})
    
    messages.error(request, 'Access denied.')
    redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:

        record = Record.objects.get(id=pk)
        
        form = AddRecordForm(request.POST or None, instance=record)
        
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully!')
            return render(request, 'record.html', {'record': record})

        return render(request, 'update_record.html', {'form': form, 'record': record})
    
    messages.error(request, 'Access denied.')
    redirect('home')