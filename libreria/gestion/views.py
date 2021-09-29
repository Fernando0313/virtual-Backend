from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet
from django.db.models.query_utils import subclasses
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import CabeceraModel, DetalleModel, ProductoModel, ClienteModel
from .serializer import( ClienteSerializer, OperacionSerializer, ProductoSerializer,
                            OperacionModelSerializer)
from rest_framework import status
from .utils import PaginacionPersonalizada
import requests as solicitudes
from os import environ
from django.db import transaction, Error
from datetime import datetime
from django.shortcuts import get_object_or_404, get_list_or_404
class PruebaController(APIView):
    def get(self, request, format=None):
        return Response(data={'message': 'Exito'}, status=200)

    def post(self, request: Request, format=None):
        # print(request.data)
        return Response(data={'message': 'Hiciste post'})


class ProductosController(ListCreateAPIView):

    queryset = ProductoModel.objects.all()

#     # pondremos la consulta de ese modelo en la bd
#     queryset = ProductoModel.objects.all()  # SELECT * FROM productos;
    serializer_class = ProductoSerializer
    pagination_class = PaginacionPersonalizada
    # def get (self,request):
    #     respuesta = self.get_queryset().filter(productoEstado=True).all()
    #     print(respuesta)
    #     respuesta_serializada = self.serializer_class(instance=respuesta,
    #     many=True)
    #     return Response(data={
    #         "message": None,
    #         "content": respuesta_serializada.data
    #         })
    def post(self, request:Request):

        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                "message":"Producto creado exitosamente",
                "content": data.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                "message": "Error al guardar el producto",
                "content": data.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
class ProductoController(APIView):
    def get(self,request, id):
        productoEncontrado = ProductoModel.objects.filter(productoId=id).first()
        
        if productoEncontrado is None:
            return Response(data={
                "message": "Producto no encontrado",
                "content": None
            },status=status.HTTP_404_NOT_FOUND)
        serializador = ProductoSerializer(instance=productoEncontrado)
        return Response(data={
            "message":None,
            "content": serializador.data
        })
    def put(self,request: Request, id):

        productoEncontrado = ProductoModel.objects.filter(productoId = id).first()
        if productoEncontrado is None:
            return Response( data={
                "message": "Producto no existe",
                "content": None
            }, status=status.HTTP_404_NOT_FOUND)

        serializador = ProductoSerializer(data=request.data)

        if serializador.is_valid():
            serializador.update(instance=productoEncontrado,
                                validated_data=serializador.validated_data)
        
            return Response(data={
                "message": "Producto actualizado exitosamente",
                "content": serializador.data
            })
        else:
            return Response(data={
                "message": "Error al actualizar el producto",
                "content": serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        
    def delete(self,request, id):
        
        productoEncontrado = ProductoModel.objects.filter(productoId = id).first()
        if productoEncontrado is None:
            return Response( data={
                "message": "Producto no existe",
                "content": None
            }, status=status.HTTP_404_NOT_FOUND)
        
        productoEncontrado.productoEstado = False
        productoEncontrado.save()
        serializador = ProductoSerializer(instance=productoEncontrado)
        return Response(data={
            "message": "producto eliminado exitosamente",
            "content": serializador.data
        })
        
        

class ClienteController(CreateAPIView):
    queryset=ClienteModel.objects.all()
    serializer_class = ClienteSerializer

    # def get(self,request):
    #     pass

    def post(self, request: Request):
        
        data: Serializer = self.get_serializer(data=request.data)
        if data.is_valid():
            # print(data.validated_data)
            # print(data.initial_data)
            # print(data.data)
            documento= data.validated_data.get('clienteDocumento')
            direccion= data.validated_data.get('clienteDireccion')
            url='https://apiperu.dev/api/'
            if len(documento) == 8:
                if direccion is None:
                    return Response(data={
                        'message':'Los clientes con DNI se debe proveer la direccion'
                    }, status=status.HTTP_400_BAD_REQUEST)
                url += 'dni/'
            elif len(documento) == 11:
                url += 'ruc/'

            resultado = solicitudes.get(url+documento, headers={
                'Content-Type':'application/json',
                'Authorization':'Bearer '+environ.get('APIPERU_TOKEN')
            }
             
            )
            # print(resultado.json())
            success =resultado.json().get('success')

            #validar si el dni existe o no
            if success is False:                
                return Response(data={
                    'message':'Documento incorrecto'
                },status=status.HTTP_400_BAD_REQUEST)
            
            data= resultado.json().get('data')
            nombre=data.get('nombre_completo') if data.get(
                'nombre_completo') else data.get('nombre_o_razon_social')
           #hacer algo similar con la direccion
            direccion = direccion if len(
                documento) == 8 else data.get('direccion_completa')

            #guardado del cliente en la bd
            nuevoCliente = ClienteModel(
                clienteNombre=nombre, clienteDocumento=documento, clienteDireccion=direccion)
            
            nuevoCliente.save()

            nuevoClienteSerializado: Serializer = self.serializer_class(
                instance=nuevoCliente)

            return Response(data={
                'message':'Cliente agregado exitosamente',
                'content': nuevoClienteSerializado.data
            })
        else:
            return Response(data={
                'message':'Error al ingresar el cliente',
                'content': data.errors
            })

class BuscadorClienteController(RetrieveAPIView):
    serializer_class = ClienteSerializer

    def get(self, request: Request):
        print(request.query_params)
        #primero validar si me esta pasando el nombre o el documento
        nombre = request.query_params.get('nombre')
        documento =request.query_params.get('documento')

        #si tengo el documento hare una busqueda todos los clientes por ese documento
        clienteEncontrado = None
        if documento:
            clienteEncontrado:  QuerySet = ClienteModel.objects.filter(
                clienteDocumento=documento)
            

            data = self.serializer_class(instance=clienteEncontrado, many=True)

            # return Response({'content':data.data})
        
        if nombre:


            if clienteEncontrado is not None:
                clienteEncontrado = clienteEncontrado.filter(
                    clienteNombre__icontains=nombre).all()
            
            else:
                clienteEncontrado = ClienteModel.objects.filter(
                    clienteNombre__icontains=nombre).all()
                

        data = self.serializer_class(instance=clienteEncontrado, many=True)
            #agregar los test para el cliente controller y su busqueda
            #dar la opcion que se pueda

        return Response(data={
            'message':'Los usuarios son:',
            'content':data.data
        })

class OperacionController(CreateAPIView):
    serializer_class = OperacionSerializer
    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            #Si el cliente existe o no por su documento
            documento=data.validated_data.get('cliente')
            clienteEncontrado = ClienteModel.objects.filter(
                clienteDocumento = documento).first()
            print(clienteEncontrado)
            detalles = data.validated_data.get('detalle')
            tipo = data.validated_data.get('tipo')

            try:
                with transaction.atomic():
                    if clienteEncontrado is None:
                        raise Error('Usuario no existe')
                    nuevaCabecera = CabeceraModel(
                        cabeceraTipo=tipo, clientes=clienteEncontrado)
                    nuevaCabecera.save()

                    for detalle in detalles:
                        producto = ProductoModel.objects.get(
                            productoId =detalle.get('producto'))

                        DetalleModel(
                            detalleCantidad = detalle.get('cantidad'),
                            detalleImporte = producto.productoPrecio *
                            detalle.get('cantidad'),
                            productos=producto,
                            cabeceras=nuevaCabecera).save()

            except Error as e:
                print(e)
                return Response(data={
                    'message': 'Error al crear la operacion',
                    'content': e.args
                })
            except Exception as exc:
                return Response(data={
                    'message' : 'Error al crear la operacion',
                    'content': exc.args
                })
                
            return Response(data={
                'message':'Operacion registrada exitosamente'
            })
        else:
            return Response(data={
                'message':'Error al crear la operacion',
                'content': data.errors
            },status=status.HTTP_400_BAD_REQUEST)

class OperacionesController(RetrieveAPIView):
    serializer_class = OperacionModelSerializer

    def get(self, request: Request, id):
        cabecera = get_object_or_404(CabeceraModel,pk=id)
        #cabecera = cabeceraModel.objects.get(cabeceraId=id)
        print(cabecera)
        cabecera_serializada = self.serializer_class(instance=cabecera)
        return Response(data={
            'message': 'La operacion es:',
            'Content': cabecera_serializada.data
        })