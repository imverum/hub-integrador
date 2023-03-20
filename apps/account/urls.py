
from django.urls import path, include
from django.contrib.auth import views as auth_views

from apps.account.views import register,usuario_deletar, usuario_edit_admin, usuario_edit_admin_ajax
from apps.usuario.views import profile_edit

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('deletar/', usuario_deletar, name='usuario_deletar'),
    path('editar/', usuario_edit_admin, name='usuario_edit_admin'),
    path('usuario_edit_admin_ajax/<int:pk>', usuario_edit_admin_ajax, name='usuario_edit_admin_ajax'),
    path('editar/<int:id>', profile_edit, name='profile_edit'),
    path('', include('django.contrib.auth.urls'))
]