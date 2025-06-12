from django.http import HttpResponse

def welcome_view(request):
    return HttpResponse("<h1>Selamat datang!</h1>")

def about_view(request):
    return HttpResponse("<h1>Halaman About</h1>")

def contacts_view(request):
    return HttpResponse("<h1>Halaman Contacts</h1>")

def alumni_view(request):
    return HttpResponse("<h1>Selamat Datang di Alumni Management System</h1>")
