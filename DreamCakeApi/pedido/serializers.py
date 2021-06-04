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
        fields = '__all__'

    def create(self, validated_data):
        costo_final = 0
        if validated_data['forma'] == 'CI':
            costo_final += 10000   
        validated_data['costo'] = costo_final
        print(validated_data['costo'])
        return Pastel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(validated_data['costo'])
        instance.forma = validated_data.get('forma', instance.forma)
        instance.num_pisos = validated_data.get('num_pisos', instance.num_pisos)
        instance.porciones = validated_data.get('porciones', instance.porciones)
        instance.masa = validated_data.get('masa', instance.masa)
        instance.relleno = validated_data.get('relleno', instance.relleno)
        instance.Cobertrura = validated_data.get('Cobertrura', instance.Cobertrura)
        instance.costo = validated_data.get('costo', instance.costo)
        
        if (instance.forma == 'CI'):
            instance.costo += 10000
        elif (instance.forma == 'CU'):
            instance.costo += 8000   
            
        instance.save()
        return instance    




    #def create(self, validated_data):
        # Modify validated_data with the value you need
        #return super().create(validated_data)

    #def update(self, instance, validated_data):
        # Modify validated_data with the value you need
        #return super().update(instance, validated_data)   

    

class PedidoSerializer(serializers.ModelSerializer):
    fecha_pedido = serializers.DateTimeField(format = '%Y-%h-%d ',read_only=True)
    class Meta:
        model = Pedido   
        fields = '__all__'

    def create(self, validated_data):
        for (key, value) in validated_data.items():
            print(key, value)
        return Pedido.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     for (key, value) in validated_data.items():
    #         print(key, value)
    #         setattr(instance, key, value)
    #     instance.save()
    #     return instance
       


class AceptarPedido(serializers.ModelSerializer):
    aceptado = serializers.BooleanField()
    class Meta:
        model = Pedido
        fields = ('aceptado',)

    def update(self, instance, validated_data):
        estado = validated_data.pop('aceptado', None)
        instance.status = (estado is not None) is True
        instance.save()
        return instance


class EstadoPedido(serializers.ModelSerializer):
    estado = serializers.IntegerField()
    class Meta:
        model = Pedido
        fields = ('estado',)
