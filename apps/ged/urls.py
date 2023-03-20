
from django.urls import path
from apps.ged.views import execucao_ld, download_arquivo, configura_ld

urlpatterns = [
    path('execucao_ld/', execucao_ld, name='execucao_ld'),
    path('download_arquivo/<int:id>', download_arquivo, name='download_arquivo'),
    path('configura_ld/', configura_ld, name='configura_ld'),

]
