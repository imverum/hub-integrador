from django.urls import path

from apps.core.conector_blob_arquivos import download_file
from apps.core.views import home

urlpatterns = [
    path('', home,name='home'),
    path('download_file/<str:file_name>/', download_file, name='download_file'),
]
