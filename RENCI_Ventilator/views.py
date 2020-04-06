from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# main entry point
def index(request):
    # render the main page
    return render(request, 'RENCI_Ventilator/index.html', {})