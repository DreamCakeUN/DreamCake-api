from rest_framework import serializers
from .models import Pedido, Pastel


class PastelSerializer(serializers.ModelSerializer):
    usuarios = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
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
        # response.usuarios.add()

        instance = super(PastelSerializer, self).create(validated_data)
        instance.usuarios.add(self.context['request'].user.id)
        return instance

    def update(self, instance, validated_data):
        # print(validated_data['costo'])
        # instance.status_pastel = validated_data.get('status_pastel', instance.status_pastel)
        instance.forma = validated_data.get('forma', instance.forma)
        instance.num_pisos = validated_data.get(
            'num_pisos', instance.num_pisos)
        instance.porciones = validated_data.get(
            'porciones', instance.porciones)
        instance.masa = validated_data.get('masa', instance.masa)
        instance.relleno = validated_data.get('relleno', instance.relleno)
        instance.cobertura = validated_data.get(
            'cobertura', instance.cobertura)
        instance.costo = validated_data.get('costo', instance.costo)

        status_pastel = validated_data.pop('status_pastel', None)
        instance.status_pastel = False if status_pastel is None else status_pastel

        if (instance.forma == 'CI'):
            instance.costo += 10000
        elif (instance.forma == 'CU'):
            instance.costo += 8000

        instance.save()
        return instance

    # def create(self, validated_data):
        # Modify validated_data with the value you need
        # return super().create(validated_data)

    # def update(self, instance, validated_data):
        # Modify validated_data with the value you need
        # return super().update(instance, validated_data)


class AddUserToPaselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pastel
        fields = ('usuarios',)
        read_only_fields = ('usuarios',)

    def update(self, instance, data):
        instance.usuarios.add(self.context['request'].user.pk)
        instance.save()
        return instance


class EditarPastelSerializer(serializers.ModelSerializer):
    usuarios = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Pastel
        fields = '__all__'

    def create(self, validated_data):
        prev = self.context['prev'].__dict__
        mod = False

        for k in validated_data.keys():
            mod = validated_data[k] is not prev[k] if not mod else False

        if not mod:
            raise serializers.ValidationError({"detail": "No se modifico"})

        instance = super().create(validated_data)
        instance.usuarios.add(self.context['request'].user.id)
        return instance


class PedidoSerializer(serializers.ModelSerializer):
    fecha_pedido = serializers.DateTimeField(
        format='%Y-%h-%d ', read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'

    def create(self, validated_data):
        validated_data['estado'] = 0
        validated_data['costo'] = validated_data['pasteles'].costo + \
            (0 if not validated_data['domiciliario'] else 5000)
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

    # def update(self, instance, validated_data):
    #     # estado = validated_data.pop('aceptado', None)
    #     instance.aceptado = validated_data['aceptado']
    #     instance.save()
    #     return instance


class EstadoPedido(serializers.ModelSerializer):
    estado = serializers.IntegerField()

    class Meta:
        model = Pedido
        fields = ('estado',)


class EditarPedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ['idpedido', 'user',
                            'aceptado', 'estado', 'fecha_pedido']

    def update(self, instance, validated_data):

        validated_data['costo'] = validated_data['pasteles'].costo + \
            (0 if not validated_data['domiciliario'] else 5000)

        if(instance.aceptado):
            raise serializers.ValidationError("El pedido ya fue aceptado")

        return super().update(instance, validated_data)
