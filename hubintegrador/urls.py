from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('users/', include('apps.usuario.urls')),
    path('accounts/', include('apps.account.urls')),
    path('unidades/', include('apps.unidade.urls')),
    path('projetos/', include('apps.projeto.urls')),
    path('ged/', include('apps.ged.urls')),
    path('fornecedores/', include('apps.fornecedores.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) # REVISAR 14