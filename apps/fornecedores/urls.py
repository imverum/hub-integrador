from django.urls import path

from apps.fornecedores.views import fornecedor_edit, fornecedor_edit_ajax, list_fornecedores, adicionar_fornecedor, fornecedor_deletar

urlpatterns = [
    path('list_fornecedores', list_fornecedores, name='list_fornecedores' ),
    path('adicionar_fornecedor', adicionar_fornecedor, name='adicionar_fornecedor' ),
    path('fornecedor_edit', fornecedor_edit, name='fornecedor_edit' ),
    path('fornecedor_deletar', fornecedor_deletar, name='fornecedor_deletar' ),
    path('fornecedor_edit_ajax/<int:pk>/', fornecedor_edit_ajax, name='fornecedor_edit_ajax' ),

]