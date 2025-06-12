from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

'''
def index(request):
    return HttpResponse("main app teste")  # Teste
'''
def index(request):
    return render(request, 'main_app/main_app.html')