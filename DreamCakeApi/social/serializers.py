from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(many= False, read_only=True)
    published_date = serializers.DateTimeField(format = '%Y-%h-%d ',read_only=True)
    class Meta:
        model = Post    
        fields = ['usuario','foto','likes','status','published_date']
                