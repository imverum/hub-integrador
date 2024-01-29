
from django.urls import path, include

from apps.cronogramacontratadas.views import api_planilha_bi_contratada, pacote_contratada_edit, contratada_edit_ajax, carga_mip, validacao_cronograma_contratdas, execucao_cronograma_contratada_deletar, execucao_cronograma_contratada_atividades, list_cronograma_contratada, register_cronograma_contratada, processo_documento_deletar, list_cargas_cronograma_contratada
from django.urls import converters




urlpatterns = [
    path('list_cronogramas/<int:id>', list_cronograma_contratada, name='list_cronograma_contratada'),
    path('register_cronograma_contratada/<int:id>', register_cronograma_contratada, name='register_cronograma_contratada'),
    path('processo_documento_deletar/', processo_documento_deletar, name='processo_documento_deletar'),

    path('list_cargas_cronograma_contratada/<int:id>', list_cargas_cronograma_contratada, name='list_cargas_cronograma_contratada'),
    path('execucao_cronograma_contratada_atividades/', execucao_cronograma_contratada_atividades, name='execucao_cronograma_contratada_atividades'),
    path('execucao_cronograma_contratada_deletar/', execucao_cronograma_contratada_deletar, name='execucao_cronograma_contratada_deletar'),
    path('validacao_cronograma_contratdas/<str:data_corte>/<int:contratada>/', validacao_cronograma_contratdas, name='validacao_cronograma_contratdas'),
    path('contratada_edit_ajax/<int:id>/', contratada_edit_ajax, name='contratada_edit_ajax'),
    path('pacote_contratada_edit/', pacote_contratada_edit, name='pacote_contratada_edit'),
    path('cade_o_op_mip/', carga_mip, name='carga_mip'),
    path('api_planilha_bi_contratada/<int:id>/', api_planilha_bi_contratada, name='api_planilha_bi_contratada'),

]