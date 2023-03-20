from django.contrib import admin


from apps.projeto.models import Projeto


class ProjetoModelAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'codigo_projeto', 'owner', 'unidade')
    search_fields = ('owner', 'unidade','codigo_projeto')
    list_filter = ('owner','unidade')


admin.site.register(Projeto, ProjetoModelAdmin)
