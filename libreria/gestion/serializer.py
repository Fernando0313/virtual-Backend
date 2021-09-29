from re import M
from typing import ClassVar
from django.db.models import fields
import requests
from rest_framework import serializers
from .models import CabeceraModel, ClienteModel, DetalleModel, ProductoModel

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        #esto vinculara el serializador con el modelo respectivo para jalar los atributos y hacer las validaciones correspondientes
        model = ProductoModel

        #indica que campos tengo que mostrar para la deserealizacion
        #fields ='__all__' => indicará que haremos uso de todas los atributos del retorno de elementos los atributos del modelo
        fields = '__all__'
        #fields=['productoNombre','ProductoPrecio']
        
        #exclude =['campo1','campo2'] => excluira tanto de la peticion como el retorno de elementos los atributos indicados
        # exclude = ['productoId']

        #no se puede utilizar los dos atributos al mismo tiempo, es decir, o usamos el exclude o usamos el fields

class ClienteSerializer(serializers.ModelSerializer):
    clienteNombre = serializers.CharField(
        max_length=45, required=False, trim_whitespace=True, read_only=True)
    clienteDireccion = serializers.CharField(
        max_length=200, required=False, trim_whitespace= True)

    class Meta:
        model = ClienteModel
        fields = '__all__'

class DetalleOperacionSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(required=True, min_value=1)

    importe = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0.01, required=True)

    producto = serializers.IntegerField(required=True, min_value=1)  

class OperacionSerializer(serializers.Serializer):
    tipo = serializers.ChoiceField(
        choices=[('V','VENTA'),('C','COMPRA')], required=True)

    cliente = serializers.IntegerField(required= True,min_value=1)

    detalle= DetalleOperacionSerializer(many=True)

class DetalleOperacionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleModel
        # fields = '__all__'
        exclude = ['cabeceras']
        depth = 1


class OperacionModelSerializer(serializers.ModelSerializer):
    cabeceraDetalles = DetalleOperacionModelSerializer(
        # source='cabeceraDetalles',
        many=True)

    class Meta:
        model = CabeceraModel
        fields = '__all__'
        #con el atributo deph indicare cuantos niveles quiero agregar para mostrar la informacion en el caso de las FKs
        depth = 1

