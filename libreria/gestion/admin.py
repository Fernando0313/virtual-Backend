from django.contrib import admin
from .models import ClienteModel, ProductoModel

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['productoId','productoNombre','productoPrecio']
    search_fields = ['productoNombre','productoUnidadMedida']
    list_filter = ['productoUnidadMedida']
    readonly_fields = ['productoId']
admin.site.register(ClienteModel)
admin.site.register(ProductoModel, ProductoAdmin)