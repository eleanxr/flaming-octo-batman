from django.shortcuts import render

from waterkit import rasterflow

def index(request):
    return render(request, 'flowviz/index.django.html')
