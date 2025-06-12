import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from alumni_app.models import Alumni

fake = Faker()

User = get_user_model()  # 🛠 Pakai custom user model kamu

graduation_year = [2018, 2019, 2020, 2021, 2022]
majors = ['Teknik Informatika', 'Sistem Informasi', 'Kesehatan', 'Pendidikan']
job_positions = ['Programmer', 'Dokter', 'Guru', 'Belum Bekerja']
companies = ['Google', 'Tokopedia', 'RS Harapan', 'Universitas Negeri', 'Belum Ada']

class Command(BaseCommand):
    help = "Generate fake alumni data"

    def add_arguments(self, parser):
        parser.add_argument('num_records', type=int, help="Jumlah alumni yang ingin dibuat")

    def handle(self, *args, **kwargs):
        num_records = kwargs['num_records']
        created_count = 0

        for _ in range(num_records):
            username = fake.unique.user_name()
            email = fake.unique.email()

            user = User.objects.create_user(
                username=username,
                email=email,
                password="password123",
                is_member=True  # ✅ Pastikan field ini memang ada di model custom user kamu
            )

            Alumni.objects.create(
                user=user,
                name=fake.name(),
                email=email,
                graduation_year=random.choice(graduation_year),
                major=random.choice(majors),
                job_position=random.choice(job_positions),
                company=random.choice(companies)
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created_count} alumni berhasil dibuat!"))
