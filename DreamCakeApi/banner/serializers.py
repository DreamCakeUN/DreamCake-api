from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner    
        fields = '__all__'

    def create(self, validated_data):
        validated_data["status"] = True
        instance = super().create(validated_data)
        return instance
        
class BannerSerializerEdit(serializers.ModelSerializer):
    class Meta:
        model = Banner    
        fields = ['status']
        