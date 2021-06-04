from rest_framework import serializers
from .models import Post, Comentario

# class PostSerializer(serializers.ModelSerializer):
#     usuario = serializers.StringRelatedField(many= False, read_only=True)
#     published_date = serializers.DateTimeField(format = '%Y-%h-%d ',read_only=True)
#     class Meta:
#         model = Post    
#         fields = ['usuario','foto','likes','status','published_date']
                
class PostSerializer(serializers.ModelSerializer):
    published_date = serializers.DateTimeField(format = '%Y-%h-%d ',read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

class ComSerializer(serializers.ModelSerializer):
    published_date = serializers.DateTimeField(format = '%Y-%h-%d ',read_only=True)

    class Meta:
        model = Comentario
        fields = '__all__'

class ModCom(serializers.ModelSerializer):
    status = serializers.BooleanField()    
    class Meta:
        model = Comentario
        fields = ('status',)

    def update(self, instance, validated_data):
        status = validated_data.pop('status', None)
        instance.status = (status is not None) is True
        instance.save()
        return instance

class ModPost(serializers.ModelSerializer):
    status = serializers.BooleanField()
    class Meta:
        model = Post
        fields = ('status',)

    def update(self, instance, validated_data):
        status = validated_data.pop('status', None)
        instance.status = (status is not None) is True
        instance.save()
        return instance