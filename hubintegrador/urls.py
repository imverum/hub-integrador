from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('users/', include('apps.usuario.urls')),
    path('accounts/', include('apps.account.urls')),
    path('unidades/', include('apps.unidade.urls')),
    path('projetos/', include('apps.projeto.urls')),
    path('ged/', include('apps.ged.urls')),
    path('fornecedores/', include('apps.fornecedores.urls')),
    path('crono_master/', include('apps.cronograma_master.urls')),
    path('master_index/', include('apps.master_index.urls')),
    path('cronograma_contratada/', include('apps.cronogramacontratadas.urls')),
]
