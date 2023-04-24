from django.urls import path

from apps.usuario.views import profile_detail_visita, profile_edit, list_user, profile_detail, adicionar_unidade, deletar_unidade, adicionar_projeto, deletar_projeto

urlpatterns = [
    path('detail/', profile_detail, name='profile_detail'),
    path('edit/<int:id>/', profile_edit, name='profile_edit'),
    path('list_user/', list_user, name='list_user'),
    path('profile_detail/', profile_detail, name='profile_detail'),
    path('profile_detail_visita/<int:id>/', profile_detail_visita, name='profile_detail_visita'),
    path('adicionar_unidade/<int:id>/', adicionar_unidade, name='adicionar_unidade'),
    path('deletar_unidade/<int:id>/', deletar_unidade, name='deletar_unidade'),
    path('adicionar_projeto/<int:id>/', adicionar_projeto, name='adicionar_projeto'),
    path('deletar_projeto/<int:id>/', deletar_projeto, name='deletar_projeto'),

]