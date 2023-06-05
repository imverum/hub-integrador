
from django.urls import path

from apps.cronograma_master.views import container_deletar, execucao_container_crono_master, projeto_crono_master, criar_container_projeto_crono_master, container_projeto_crono_master, execucao_cronograma_master_baseline, execucao_cronograma_master, execucao_cronograma_master_crono, exportar_log_crono_master

urlpatterns = [
    path('execucao_cronograma_master/', execucao_cronograma_master, name='execucao_cronograma_master'),
    path('execucao_cronograma_master_crono/', execucao_cronograma_master_crono, name='execucao_cronograma_master_crono'),
    path('execucao_cronograma_master_baseline/', execucao_cronograma_master_baseline, name='execucao_cronograma_master_baseline'),
    path('exportar_log_crono_master/<int:id>/', exportar_log_crono_master, name='exportar_log_crono_master'),
    path('exportar_log_crono_master/<int:id>/', exportar_log_crono_master, name='exportar_log_crono_master'),
    path('container_projeto_crono_master/<int:id>/', container_projeto_crono_master, name='container_projeto_crono_master'),
    path('criar_container_projeto_crono_master/<int:id>/', criar_container_projeto_crono_master, name='criar_container_projeto_crono_master'),
    path('projeto_crono_master/<int:id>/', projeto_crono_master, name='projeto_crono_master'),
    path('execucao_container_crono_master/<int:id>/', execucao_container_crono_master, name='execucao_container_crono_master'),
    path('container_deletar/<int:id>/', container_deletar, name='container_deletar'),

]
