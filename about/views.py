from django.shortcuts import render

def about(request):
    return render(request, 'alumni_management/about.html')
