from django.shortcuts import render

def spa_index(request):
    return render(request, 'frontend_app_spa/index.html')
