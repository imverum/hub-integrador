from django.urls import path

from apps.unidade.views import list_unidades, unidade_detail

urlpatterns = [
    path('unidade_list/', list_unidades, name='list_unidades'),
    path('unidade_detail/<int:id>', unidade_detail, name='unidade_detail'),

]