from django.shortcuts import render,redirect
from accounts.forms import UserRegistrationForm,UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .models import User

# Create your views here.

def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      messages.success(request,"Ви успішно зареєструвались")
      return redirect('accounts:login')
  else:
    form = UserRegistrationForm()
  return render(request,'accounts/register.html',{'form':form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
           
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                except User.DoesNotExist:
                    username = None  
                    messages.error(request, 'Цей email не зареєстрований')
                    return render(request, 'accounts/login.html', {'form': form})  
            else:
                if not User.objects.filter(username=username).exists():
                    messages.error(request, 'Це ім’я користувача не зареєстровано')
                    return render(request, 'accounts/login.html', {'form': form})
           
            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Неправильний пароль')
    else:
        form = UserLoginForm()
       
    return render(request, 'accounts/login.html', {'form': form})     
 
 
def logout(request):
  django_logout(request)
  return redirect('/')