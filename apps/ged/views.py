from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from apps.ged.etl_ld import run_ld
from apps.ged.forms import LDFormCarga, ConfiguraLdForm
from apps.ged.models import ExecucaoLD, ConfiguraLd
from apps.projeto.models import Projeto
from apps.usuario.models import Profile









@csrf_exempt
@login_required
def execucao_ld(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)
    if request.method == 'POST':

        form_projeto_ld = LDFormCarga(request.POST or None)

        if form_projeto_ld.is_valid():
            ld = form_projeto_ld.save(commit=False)
            ld.projeto = projeto
            ld.unidade = projeto.unidade
            ld.owner = projeto.unidade.owner
            ld.profile = profile

            ld.tipo = 'LD'

            arquivold_file = request.FILES.get('arquivold')
            if arquivold_file != None:
                ExecucaoLD.objects.filter(id=ld.id).update(arquivold=arquivold_file)
                run_ld(arquivold_file)


            ld.status = 'Finalizado'
            ld.save()


            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(LDFormCarga.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:

        pass


@csrf_exempt
@login_required
def download_arquivo(request, id):
    arquivold = get_object_or_404(ExecucaoLD, id=id)
    if not arquivold.arquivold:
        raise Http404

    response = HttpResponse(arquivold.arquivold, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{arquivold.arquivold}"'

    return response

@csrf_exempt
def configura_ld(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)

    configura_ld_instance = ConfiguraLd.objects.get(projeto=projeto)
    form_configura = ConfiguraLdForm(request.POST or None, instance=configura_ld_instance)
    if request.method == "POST":
        if form_configura.is_valid():
            form_configura.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
