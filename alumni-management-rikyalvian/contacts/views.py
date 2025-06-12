from django.shortcuts import render

def contacts(request):
    return render(request, 'alumni_management/contacts.html')
