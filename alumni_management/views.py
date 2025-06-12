from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from .forms import CustomUserCreationForm, CustomLoginForm
from .models import User

# Registrasi User
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')  # Halaman setelah registrasi berhasil


# Login Custom
class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'


# Logout
class CustomLogoutView(LogoutView):
    next_page = 'login'


# Dashboard, hanya bisa diakses oleh user yang sudah login
@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_admin:
            # Jika user admin, tampilkan semua alumni
            alumni_list = User.objects.filter(is_member=True)
            context['alumni_list'] = alumni_list
        return context


# View untuk Alumni Profile
@login_required
def alumni_profile(request):
    if request.user.is_member:  # Cek apakah user adalah alumni
        return render(request, 'alumni_profile.html', {'user': request.user})
    else:
        return HttpResponseForbidden("You do not have permission to view this page.")


# Edit Profil Alumni
@login_required
def edit_alumni_profile(request):
    if request.user.is_member:
        if request.method == 'POST':
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.save()
            return redirect('alumni_profile')
        return render(request, 'edit_alumni_profile.html', {'user': request.user})
    else:
        return HttpResponseForbidden("You do not have permission to view this page.")
