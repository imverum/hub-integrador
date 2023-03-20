from django.contrib import admin
from apps.usuario.models import Profile


class UsuarioProfileModelAdmin(admin.ModelAdmin):

    list_display = ('user','nome', 'user_photo')



admin.site.register(Profile, UsuarioProfileModelAdmin)
