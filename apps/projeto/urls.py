from django.urls import path

from apps.projeto.views import projeto_deletar, register_projeto, projeto_detail, projeto_edit_ajax, projeto_edit

urlpatterns = [
    path('projeto_detail/<int:id>/', projeto_detail, name='projeto_detail'),
    path('register_projeto/', register_projeto, name='register_projeto'),
    path('projeto_edit_ajax/<int:pk>/', projeto_edit_ajax, name='projeto_edit_ajax'),
    path('projeto_edit/', projeto_edit, name='projeto_edit'),
    path('projeto_deletar/', projeto_deletar, name='projeto_deletar'),

]