from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.core.models import Usuario_Unidade, Unidade
from apps.projeto.forms import ProjetoFormAdd
from apps.projeto.models import Projeto, Usuario_Projeto
from apps.usuario.models import Profile
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def list_unidades(request):
    usuario = request.user
    profile = Profile.objects.get(user=usuario)
    unidades = Usuario_Unidade.objects.filter(usuario=usuario)


    return render(request, 'list_unidades.html', {'unidades':unidades, 'profile':profile})

@login_required
@csrf_exempt
def unidade_detail(request, id):
    unidade = Unidade.objects.get(id=id)
    qtd_usuarios = Usuario_Unidade.objects.filter(unidade=unidade).count()
    qtd_projetos = 10
    form_projeto = ProjetoFormAdd(request.POST or None)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)
    projetos = Usuario_Projeto.objects.filter(usuario=usuario, unidade=unidade)



    contexto = {'unidade':unidade, 'qtd_usuarios':qtd_usuarios,'qtd_projetos':qtd_projetos, 'projetos':projetos, 'form_projeto':form_projeto, 'profile':profile}


    return render(request, 'unidade_detail.html', contexto)