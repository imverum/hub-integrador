
from django.urls import path

from apps.cronograma_master.views import execucao_cronograma_master, execucao_cronograma_master_crono, exportar_log_crono_master

urlpatterns = [
    path('execucao_cronograma_master/', execucao_cronograma_master, name='execucao_cronograma_master'),
    path('execucao_cronograma_master_crono/', execucao_cronograma_master_crono, name='execucao_cronograma_master_crono'),
    path('exportar_log_crono_master/<int:id>/', exportar_log_crono_master, name='exportar_log_crono_master'),

]
