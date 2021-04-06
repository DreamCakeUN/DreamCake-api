from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Template, Context
from .models import Banner

def home(request):
    main_template = loader.get_template('index.html')
    promos = Banner.objects.all()
    context = {"Promociones": promos}
    index_page = main_template.render(context)
    return HttpResponse(index_page)

