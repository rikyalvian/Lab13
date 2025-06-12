from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Alumni
from .forms import AlumniForm

# Fungsi pembantu untuk mengecek apakah user adalah admin
def user_is_admin(user):
    return getattr(user, 'is_admin', False) or user.is_staff or user.is_superuser

# ======= HALAMAN STATIS =======
def home(request):
    return render(request, 'alumni_management/home.html')

def about(request):
    return render(request, 'alumni_management/about.html')

def contacts(request):
    return render(request, 'alumni_management/contacts.html')

# ======= DASHBOARD PUBLIK, CRUD HANYA UNTUK ADMIN =======
def dashboard(request):
    qs = Alumni.objects.all()
    year = request.GET.get('year')
    major = request.GET.get('major')

    if year:
        qs = qs.filter(graduation_year=year)
    if major:
        qs = qs.filter(major=major)

    total_alumni = qs.count()
    angkatan = qs.values('graduation_year').annotate(total=Count('id')).order_by('graduation_year')
    pekerjaan = qs.values('job_position').annotate(count=Count('id')).order_by('-count')
    bidang_keys = ['Programmer', 'Dokter', 'Guru', 'Manager']
    bidang = [{'field': kw, 'count': qs.filter(job_position__icontains=kw).count()} for kw in bidang_keys]
    top_perusahaan = qs.values('company').annotate(jumlah=Count('id')).order_by('-jumlah')[:5]

    context = {
        'total_alumni': total_alumni,
        'angkatan_labels': [str(x['graduation_year']) for x in angkatan],
        'angkatan_data': [x['total'] for x in angkatan],
        'pekerjaan_labels': [x['job_position'] for x in pekerjaan],
        'pekerjaan_data': [x['count'] for x in pekerjaan],
        'bidang_labels': [x['field'] for x in bidang],
        'bidang_data': [x['count'] for x in bidang],
        'perusahaan_labels': [x['company'] for x in top_perusahaan],
        'perusahaan_data': [x['jumlah'] for x in top_perusahaan],
        'filters': {'year': year or '', 'major': major or ''},
        'all_years': Alumni.objects.values_list('graduation_year', flat=True).distinct().order_by('graduation_year'),
        'all_majors': Alumni.objects.values_list('major', flat=True).distinct(),
        'can_crud': user_is_admin(request.user),
    }
    return render(request, 'dashboard/dashboard.html', context)

# ======= PROFIL ALUMNI =======
def alumni_profile(request):
    if user_is_admin(request.user):
        return redirect('list_alumni')
    profile = get_object_or_404(Alumni, user=request.user)
    return render(request, 'alumni_management/profile.html', {'alumni': profile})

class AlumniProfileUpdateView(UpdateView):
    model = Alumni
    form_class = AlumniForm
    template_name = 'alumni_management/update_alumni.html'
    success_url = reverse_lazy('alumni_profile')

    def get_object(self):
        return get_object_or_404(Alumni, user=self.request.user)

# ======= CRUD ALUMNI (ADMIN SAJA) =======
class AlumniListView(ListView):
    model = Alumni
    template_name = 'alumni_management/list_alumni.html'
    context_object_name = 'alumni_list'

    def dispatch(self, request, *args, **kwargs):
        if not user_is_admin(request.user):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class AlumniDetailView(DetailView):
    model = Alumni
    template_name = 'alumni_management/detail_alumni.html'
    context_object_name = 'alumni'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (user_is_admin(request.user) or obj.user == request.user):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class AlumniCreateView(CreateView):
    model = Alumni
    form_class = AlumniForm
    template_name = 'alumni_management/add_alumni.html'
    success_url = reverse_lazy('alumni_profile')

    def dispatch(self, request, *args, **kwargs):
        if not user_is_admin(request.user) and Alumni.objects.filter(user=request.user).exists():
            return redirect('alumni_profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if not user_is_admin(self.request.user):
            form.instance.user = self.request.user
        return super().form_valid(form)

class AlumniUpdateView(UpdateView):
    model = Alumni
    form_class = AlumniForm
    template_name = 'alumni_management/update_alumni.html'
    success_url = reverse_lazy('alumni_profile')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (user_is_admin(request.user) or obj.user == request.user):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class AlumniDeleteView(DeleteView):
    model = Alumni
    template_name = 'alumni_management/delete_alumni.html'
    success_url = reverse_lazy('list_alumni')

    def dispatch(self, request, *args, **kwargs):
        if not user_is_admin(request.user):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

# ======= AJAX UNTUK MODAL =======
@require_GET
def alumni_detail_json(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    if not (user_is_admin(request.user) or alumni.user == request.user):
        return JsonResponse({'error': 'Tidak punya akses'}, status=403)

    data = {
        'name': alumni.name,
        'email': alumni.email,
        'graduation_year': alumni.graduation_year,
        'major': alumni.major,
        'job_position': alumni.job_position,
        'company': alumni.company,
    }
    return JsonResponse(data)
