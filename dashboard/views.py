import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from alumni_app.models import Alumni
from .models import DashboardLog

@login_required
def dashboard_view(request):
    year_filter  = request.GET.get('year', '')
    major_filter = request.GET.get('major', '')

    qs = Alumni.objects.all()
    if year_filter:
        qs = qs.filter(graduation_year=year_filter)
    if major_filter:
        qs = qs.filter(major=major_filter)

    total_alumni = qs.count()
    
    # ✅ Ganti alumni -> qs
    bekerja = qs.filter(status_kerja=True).count()
    persentase_bekerja = round((bekerja / total_alumni) * 100) if total_alumni > 0 else 0

    # ✅ Ganti alumni -> qs, dan 'tahun_lulus' -> 'graduation_year'
    angkatan_terbanyak = (
        qs.values('graduation_year')
        .annotate(jumlah=Count('id'))
        .order_by('-jumlah')
        .first()
    )

    angkatan_qs = (
        qs
        .values('graduation_year')
        .annotate(total=Count('id'))
        .order_by('graduation_year')
    )
    labels_angkatan = [item['graduation_year'] for item in angkatan_qs]
    data_angkatan   = [item['total'] for item in angkatan_qs]

    pekerjaan_qs = (
        qs
        .values('job_position')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    labels_pekerjaan = [item['job_position'] for item in pekerjaan_qs]
    data_pekerjaan   = [item['count'] for item in pekerjaan_qs]

    bidang_keywords = ['Programmer', 'Dokter', 'Guru', 'Belum Bekerja']
    labels_bidang   = bidang_keywords
    data_bidang     = [qs.filter(job_position__icontains=kw).count() for kw in bidang_keywords]

    perusahaan_qs = (
        qs
        .values('company')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    labels_perusahaan = [item['company'] for item in perusahaan_qs]
    data_perusahaan   = [item['count'] for item in perusahaan_qs]

    angkatan_years = Alumni.objects.values_list('graduation_year', flat=True).distinct().order_by('graduation_year')
    majors         = Alumni.objects.values_list('major', flat=True).distinct()

    if request.user.is_authenticated:
        filters = {'year': year_filter, 'major': major_filter}
        DashboardLog.objects.create(user=request.user, filters_used=json.dumps(filters))

    context = {
        'total_alumni': total_alumni,
        'persentase_bekerja': persentase_bekerja,
        'angkatan_terbanyak': angkatan_terbanyak['graduation_year'] if angkatan_terbanyak else '—',
        'angkatan_years': angkatan_years,
        'majors': majors,
        'year_filter': year_filter,
        'major_filter': major_filter,
        'angkatan_labels': json.dumps(labels_angkatan),
        'angkatan_data': json.dumps(data_angkatan),
        'pekerjaan_labels': json.dumps(labels_pekerjaan),
        'pekerjaan_data': json.dumps(data_pekerjaan),
        'bidang_labels': json.dumps(labels_bidang),
        'bidang_data': json.dumps(data_bidang),
        'perusahaan_labels': json.dumps(labels_perusahaan),
        'perusahaan_data': json.dumps(data_perusahaan),
    }
    return render(request, 'dashboard/dashboard.html', context)
