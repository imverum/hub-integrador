
from django.urls import path
from apps.ged.views import execucao_ged, fluxo_ged_devolucao_deletar, fluxo_ged_devolucao_edit, fluxo_ged_devolucao_edit_ajax,adicionar_fluxo_devolucao_ged, list_fluxo_retorno, configura_ged, exportar_log, fluxo_ged_edit, fluxo_ged_edit_ajax, list_fluxo, execucao_ld, download_arquivo, configura_ld, adicionar_fluxo_ged, fluxo_ged_deletar

urlpatterns = [
    path('execucao_ld/', execucao_ld, name='execucao_ld'),
    path('download_arquivo/<int:id>', download_arquivo, name='download_arquivo'),
    path('configura_ld/', configura_ld, name='configura_ld'),
    path('configura_ged/', configura_ged, name='configura_ged'),
    path('list_fluxo/', list_fluxo, name='list_fluxo'),
    path('adicionar_fluxo_ged/', adicionar_fluxo_ged, name='adicionar_fluxo_ged'),
    path('fluxo_ged_deletar/', fluxo_ged_deletar, name='fluxo_ged_deletar'),
    path('fluxo_ged_edit_ajax/<int:pk>', fluxo_ged_edit_ajax, name='fluxo_ged_edit_ajax'),
    path('fluxo_ged_edit/', fluxo_ged_edit, name='fluxo_ged_edit'),
    path('execucao_ged/', execucao_ged, name='execucao_ged'),
    path('exportar_log/<int:id>/', exportar_log, name='exportar_log'),
    path('list_fluxo_retorno/', list_fluxo_retorno, name='list_fluxo_retorno'),
    path('adicionar_fluxo_devolucao_ged/', adicionar_fluxo_devolucao_ged, name='adicionar_fluxo_devolucao_ged'),
    path('fluxo_ged_devolucao_edit_ajax/<int:pk>', fluxo_ged_devolucao_edit_ajax, name='fluxo_ged_devolucao_edit_ajax'),
    path('fluxo_ged_devolucao_edit/', fluxo_ged_devolucao_edit, name='fluxo_ged_devolucao_edit'),
    path('fluxo_ged_devolucao_deletar/', fluxo_ged_devolucao_deletar, name='fluxo_ged_devolucao_deletar'),

]
