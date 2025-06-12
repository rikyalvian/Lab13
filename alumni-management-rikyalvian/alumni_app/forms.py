from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Alumni

User = get_user_model()

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        exclude = ['user']
        fields = ['name', 'email', 'graduation_year', 'major', 'job_position', 'company', 'photo', 'phone_number', 'linkedin']
        widgets = {
            'graduation_year': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Masukkan email yang valid."
    )
    # Field profil alumni sesuai model sederhana
    name = forms.CharField(label="Nama Lengkap", max_length=100)
    graduation_year = forms.IntegerField(label="Tahun Lulus")
    major = forms.CharField(label="Jurusan", max_length=100)
    job_position = forms.CharField(label="Posisi Pekerjaan", max_length=100)
    company = forms.CharField(label="Perusahaan", max_length=100)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'name', 'graduation_year', 'major', 'job_position', 'company'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_member = True
        user.is_admin = False
        if commit:
            user.save()
            # buat profil alumni otomatis
            Alumni.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email'],
                graduation_year=self.cleaned_data['graduation_year'],
                major=self.cleaned_data['major'],
                job_position=self.cleaned_data['job_position'],
                company=self.cleaned_data['company']
            )
        return user
