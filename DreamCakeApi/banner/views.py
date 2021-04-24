from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Template, Context
from django.views import View
from django.http import JsonResponse
from .models import Banner

# Create your views here.

class photoViewList(View):
    def get(self, request):
        #main_template = loader.get_template('index.html')
        promos = Banner.objects.all()
        #context = {"Promociones": promos}
        #index_page = main_template.render(context)
        #return HttpResponse(index_page)
        return JsonResponse(list (promos.values()), safe = False)