
from django.urls import path, include


from django.urls import converters

from apps.controlecompras.views import list_cargas_bom_compras

urlpatterns = [
    path('list_cargas_bom_compras/<int:id>', list_cargas_bom_compras, name='list_cargas_bom_compras'),
]