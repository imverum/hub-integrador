from django.contrib import admin

from apps.core.models import Unidade, Owner


class UnidadeInline(admin.TabularInline):
    model = Unidade
    extra = 1


class OwnerModelAdmin(admin.ModelAdmin):
    inlines = [UnidadeInline]
    list_display = ('owner', 'ativo')


admin.site.register(Owner, OwnerModelAdmin)