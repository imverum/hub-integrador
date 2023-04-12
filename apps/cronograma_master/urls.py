
from django.urls import path

from apps.cronograma_master.views import execucao_cronograma_master_xer, execucao_cronograma_master, execucao_cronograma_master_crono

urlpatterns = [
    path('execucao_cronograma_master/', execucao_cronograma_master, name='execucao_cronograma_master'),
    path('execucao_cronograma_master_crono/', execucao_cronograma_master_crono, name='execucao_cronograma_master_crono'),
    path('execucao_cronograma_master_xer/', execucao_cronograma_master_xer, name='execucao_cronograma_master_xer'),


]
