from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.is_member = True  # tandai sebagai alumni biasa
            user.save()

            login(request, user)
            messages.success(request, "Registrasi berhasil! Silakan lengkapi profil alumni Anda.")
            return redirect('add_alumni')  # arahkan ke form tambah data alumni
        else:
            messages.error(request, "Registrasi gagal. Silakan periksa kembali.")
    else:
        form = UserRegisterForm()
    
    return render(request, 'usermanagement/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('dashboard')
            else:
                return redirect('alumni_profile')
        else:
            messages.error(request, "Login gagal. Username atau password salah.")
    
    return render(request, 'usermanagement/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Anda berhasil logout.")
    return redirect('login')
