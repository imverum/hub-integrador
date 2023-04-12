from django import template
from django.contrib.auth.models import User

from apps.core.models import Usuario_Unidade, Unidade
from apps.projeto.models import Projeto

register = template.Library()

@register.filter
def tipo_registro(registro):
    ROLE_CHOICE = {
        1: 'Administrador',
        2: 'Usuário',
    }

    return ROLE_CHOICE[registro]


@register.filter
def status_usuario(user_id):
    user = User.objects.get(id=user_id)
    if user.is_active == True:
        status = "Ativo"
    else:
        status = "Inativo"

    return status


@register.filter
def qtd_usuario_unidade(unidade_id):
    unidade = Unidade.objects.get(id=unidade_id)
    qtd_user = Usuario_Unidade.objects.filter(unidade=unidade).count()

    return qtd_user

@register.filter
def qtd_projeto_unidade(unidade_id):
    unidade = Unidade.objects.get(id=unidade_id)
    qtd_projeto = Projeto.objects.filter(unidade=unidade).count()

    return qtd_projeto


@register.filter
def status_projeto(projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    if projeto.ativo == True:
        status = "Ativo"
    else:
        status = "Inativo"

    return status


@register.filter
def render_sim_nao(id):
    if id == 1:
        render = "SIM"
    else:
        render = "NÃO"

    return render


@register.filter
def base_name(file_name):
    if file_name == "media/RelatorioCBMM_P22113_MQbq15H.xlsx":
        return "Arquivo não encontrado"
    try:
        caminho=str(file_name)
    except:
        caminho="Arquivo não encontrado"

    print(caminho)
    return caminho