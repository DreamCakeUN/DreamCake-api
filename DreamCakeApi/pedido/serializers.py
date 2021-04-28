from rest_framework import serializers
from .models import Pedido, Pastel

class PastelSerializer(serializers.ModelSerializer):
    usuarios = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
     )
    #published_date = serializers.DateTimeField(format = '%Y-%h-%d ',read_only=True)
    class Meta:
        model = Pastel    
        fields = ['usuarios','costo','status_pastel','num_pisos', 'porciones']

    def create(self, validated_data):
        return Pastel(**validated_data)

    

class PedidoSerializer(serializers.ModelSerializer):
    pasteles = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id'
     )
    usuario = serializers.StringRelatedField(many= False, read_only=True)
    fecha_pedido = serializers.DateTimeField(format = '%Y-%h-%d ',read_only=True)

    class Meta:
        model = Pedido    
        fields = ['pasteles','usuario','direccion','costo','status','correo_asociado','fecha_pedido', 'comentario']
