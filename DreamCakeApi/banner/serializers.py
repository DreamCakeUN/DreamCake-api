from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner    
        fields = ['title','text','abstract','publication_date','image']
        