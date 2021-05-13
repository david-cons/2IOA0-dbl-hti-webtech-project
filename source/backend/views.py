
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def baseData(request):
    file = request.FILES['csv_data']
    return JsonResponse({'size': file.size})
