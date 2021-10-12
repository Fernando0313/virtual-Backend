from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils import serializer_helpers
from .serializers import ImagenSerializer, RegistroSerializer, PlatoSerializer, VentaSerializer
from .models import DetallePedidoModel, PedidoModel, PlatoModel, UsuarioModel
from os import remove
from django.db.models import ImageField
from django.db import transaction
from django.conf import settings


class RegistroController(CreateAPIView):
    serializer_class = RegistroSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        
        if data.is_valid():
            data.save()
            return Response(data={
                'message': 'Usuario creado exitosamente',
                'content': data.data
            })
        else:
            return Response(data={
                'message': 'Error al crear el usuario',
                'content': data.errors
            })

class PlatosController(ListCreateAPIView):
    serializer_class = PlatoSerializer
    queryset =PlatoModel.objects.all()

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'content':data.data,
                'content': 'Plato creado exitosamento'
            })
        else:
            return Response(data={
                'message': 'Error al crear el plato',
                'content': data.errors
            }, status=400)
    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(data={
            'message': None,
            'content': data.data
        })
class SubirImagenController(ListCreateAPIView):
    serializer_class = ImagenSerializer

    def post(self, request: Request):
        print(request.FILES)
        data = self.serializer_class(data=request.FILES)

        if data.is_valid():
            archivo = data.save()
            url = request.META.get('HTTP_HOST')

            return Response(data={
                'message': 'Archivo subido exitosamente',
                'content': url + archivo
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message': 'Error al crear el archivo',
                'content': data.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        data = self.serializer_class(instance=self.get_queryset(),many=True)
        return Response(data={
            'message':None,
            'content':data.data
        })



class PlatoController(RetrieveUpdateDestroyAPIView):
    serializer_class = PlatoSerializer
    queryset = PlatoModel.objects.all()

    def patch(self, request, id):
        # actualizacion parcial
        pass

    def put(self, request, id):
        # hacer el put actualizacion total
        pass

    def get(self, request, id):
        platoEncontrado = self.get_queryset().filter(platoId=id).first()

        if not platoEncontrado:
            return Response(data={
                'message': 'Plato no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        data = self.serializer_class(instance=platoEncontrado)

        return Response(data={
            'content': data.data
        })

    def delete(self, request, id):

        platoEncontrado = self.get_queryset().filter(platoId=id).first()
        if not platoEncontrado:
            return Response(data={
                'message': 'Plato no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            data = platoEncontrado.delete()
            remove(settings.MEDIA_ROOT / str(platoEncontrado.platoFoto))
        except Exception as e:
            print(e)

        # data = PlatoModel.objects.filter(platoId=id).delete()
        # (num_registros_eliminados, { platoModel: id })
        print(data)
        return Response(data={
            'message': 'Plato eliminado exitosamente'
        })
class VentaController(CreateAPIView):
    serializer_class = VentaSerializer

    def post(self, request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            cliente_id = data.validated_data.get('cliente_id')
            vendedor_id = data.validated_data.get('vendedor_id')
            detalles = data.validated_data.get('detalle')
            try:
                with transaction.atomic():
                    cliente = UsuarioModel.objects.filter(
                        usuarioId=cliente_id).first()

                    vendedor = UsuarioModel.objects.filter(
                        usuarioId=vendedor_id).first()

                    if not cliente or not vendedor:
                        raise Exception('Usuarios incorrectos')

                    if cliente.usuarioTipo != 3:
                        raise Exception('Cliente no corresponde el tipo')

                    if vendedor.usuarioTipo == 3:
                        raise Exception('Vendedor no corresponde el tipo')

                    pedido = PedidoModel(
                        pedidoTotal=0, cliente=cliente, vendedor=vendedor)

                    pedido.save()
                    for detalle in detalles:
                        plato_id = detalle.get('producto_id')
                        cantidad = detalle.get('cantidad')
                        plato = PlatoModel.objects.filter(
                            platoId=plato_id).first()
                        if not plato:
                            raise Exception('Plato {} no existe'.format(
                                plato_id))
                        if cantidad > plato.platoCantidad:
                            raise Exception(
                                'No hay suficiente cantidad para el producto {}'.format(plato.platoNombre))
                        plato.platoCantidad = plato.platoCantidad - cantidad
                        plato.save()
                        detallePedido = DetallePedidoModel(detalleCantidad=cantidad,
                                                           detalleSubTotal=plato.platoPrecio * cantidad,
                                                           plato=plato,
                                                           pedido=pedido)
                        detallePedido.save()
                        pedido.pedidoTotal += detallePedido.detalleSubTotal
                        pedido.save()
                return Response(data={
                    'message': 'Venta agregada exitosamente'
                })

            except Exception as e:
                return Response(data={
                    'message': e.args
                }, status=400)

        else:
            return Response(data={
                'message': 'Error al agregar la venta',
                'content': data.errors
            })