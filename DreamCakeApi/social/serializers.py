from rest_framework import serializers
from .models import Post, Comentario
from users.serializers import PublicUserDetailSerilizer

# class PostSerializer(serializers.ModelSerializer):
#     usuario = serializers.StringRelatedField(many= False, read_only=True)
#     published_date = serializers.DateTimeField(format = '%Y-%h-%d ',read_only=True)
#     class Meta:
#         model = Post    
#         fields = ['usuario','foto','likes','status','published_date']
                
class PostSerializer(serializers.ModelSerializer):
    published_date = serializers.DateTimeField(format = '%Y-%h-%d ',read_only=True)

    # usuario = PublicUserDetailSerilizer()
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ("usuario", )

    def create(self, validated_data):
        validated_data["usuario"] = self.context['request'].user
        instance = super().create(validated_data)
        return instance

class ComSerializer(serializers.ModelSerializer):
    published_date = serializers.DateTimeField(format = '%Y-%h-%d ',read_only=True)

    class Meta:
        model = Comentario
        fields = '__all__'
        read_only_fields = ("usuario", )

    def create(self, validated_data):
        validated_data["usuario"] = self.context['request'].user
        instance = super().create(validated_data)
        return instance

class ModCom(serializers.ModelSerializer):
    status = serializers.BooleanField()    
    class Meta:
        model = Comentario
        fields = ('status',)

    def update(self, instance, validated_data):
        status = validated_data.pop('status', None)
        instance.status = False if status is None else status
        instance.save()
        return instance

class ModPost(serializers.ModelSerializer):
    status = serializers.BooleanField()
    class Meta:
        model = Post
        fields = ('status',)

    def update(self, instance, validated_data):
        status = validated_data.pop('status', None)
        instance.status = False if status is None else status
        instance.save()
        return instance

class LikePost(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['likes']
        read_only_fields = ['likes']

    def update(self, instance, validated_data):
        validated_data['likes'] = instance.likes + 1
        return super().update(instance, validated_data)