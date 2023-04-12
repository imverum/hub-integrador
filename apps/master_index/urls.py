from django.urls import path


from apps.master_index.views import execucao_master_index_pacotes, execucao_master_index_cwa

urlpatterns = [
    path('execucao_master_index_pacotes', execucao_master_index_pacotes,name='execucao_master_index_pacotes'),
    path('execucao_master_index_cwa', execucao_master_index_cwa,name='execucao_master_index_cwa'),
]
