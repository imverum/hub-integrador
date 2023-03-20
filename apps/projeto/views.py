from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from apps.core.models import Unidade
from apps.ged.forms import LDFormCarga, ConfiguraLdForm
from apps.ged.models import ExecucaoLD, ConfiguraLd
from apps.projeto.forms import ProjetoFormAdd, GEDFormCarga
from apps.projeto.models import Projeto, Usuario_Projeto
from apps.usuario.models import Profile
from django.contrib import messages

@login_required
def projeto_detail(request, id):
    pass

@login_required
def register_projeto(request):
    unidade_id = request.POST.get("unidade_id")
    unidade = Unidade.objects.get(id=unidade_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)
    if request.method == 'POST':

        form_projeto = ProjetoFormAdd(request.POST or None)

        if form_projeto.is_valid():
            projeto = form_projeto.save(commit=False)
            projeto.unidade = unidade
            projeto.owner = profile.owner
            projeto.save()

            projeto_user = Usuario_Projeto.objects.create(
             projeto=projeto,
             usuario=usuario,
             unidade=unidade,
            )

            projeto_ld = ConfiguraLd.objects.create(
             owner=profile.owner,
             unidade=unidade,
             projeto=projeto,
             documento='Nª CLIENTE',
             numero_contratada='Nª BRASS',
             titulo='DESCRIÇÃO',
             status_ld='STATUS',
             codigo_atividade='ITEM CR',
             sk='sk',
             data_emissão_inicial_prevista='TÉRMINO LINHA DE BASE',
             paginas='PÁGINAS',
             a1_equivalente='A1 EQ.',
            )

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def projeto_edit_ajax(request, pk):
    projeto = Projeto.objects.get(id=pk)

    data = {
        'projeto': projeto.projeto,
        'codigo_projeto': projeto.codigo_projeto,
        'descricao': projeto.descricao,
        'inicio_projeto': projeto.inicio_projeto,
        'termino_projeto': projeto.termino_projeto,
    }

    return JsonResponse(data)

@login_required
def projeto_edit(request):
    id = request.POST.get("id_edit")
    projeto = Projeto.objects.get(id=id)
    form_projeto = ProjetoFormAdd(request.POST or None, instance=projeto)

    if request.method == "POST":

        if form_projeto.is_valid():
            edit_projeto = form_projeto.save(commit=False)
            try:
                edit_projeto.save()
            except:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@csrf_exempt
@login_required
def projeto_deletar(request):
    projeto_id_delet = request.POST.get('id_delet')
    projeto = Projeto.objects.get(id=projeto_id_delet)
    projeto.delete()
    messages.success(request, "Restricion deleted successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required
def projeto_detail(request, id):
    projeto = Projeto.objects.get(id=id)

    form_projeto_ged = GEDFormCarga(request.POST or None)
    form_projeto_ld = LDFormCarga(request.POST or None)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)
    execucoes = ExecucaoLD.objects.filter(projeto=projeto)
    configura_ld_instance = ConfiguraLd.objects.get(projeto=projeto)
    form_configura = ConfiguraLdForm(request.POST or None, instance=configura_ld_instance)




    contexto = {'projeto':projeto, 'form_configura':form_configura, 'execucoes':execucoes, 'form_projeto_ged':form_projeto_ged,'form_projeto_ld':form_projeto_ld ,'usuario':usuario, 'profile':profile}


    return render(request, 'projeto_detail.html', contexto)


