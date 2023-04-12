import os

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
import io

from apps.core.conector_blob_arquivos import conector_blob
from apps.fornecedores.models import Fornecedores
from apps.ged.etl_ged import run_ged
from apps.ged.etl_ld import run_ld, criar_planilha_log
from apps.ged.forms import LDFormCarga, ConfiguraLdForm, FluxoRegisterForm, ConfiguraGEDForm, FluxoDevolucaoForm, GEDFormCarga
from apps.ged.models import ExecucaoLD, ConfiguraLd, FluxoEmissao, ConfiguraGED, FluxoDevolucaoGED
from apps.projeto.models import Projeto
from apps.usuario.models import Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from azure.storage.blob import BlobServiceClient



# obtenha a instância BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=verumsys;AccountKey=zsjENq7RHecRcbSOGJrIjaXdV/z4kh0KtTsf/J/xy1FeANFcnXSnh6LDytspbpbF4Q5OwJOK4UnC+ASt4uembg==;EndpointSuffix=core.windows.net")

@csrf_exempt
@login_required
def list_fluxo(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    fluxos = FluxoEmissao.objects.filter(owner=profile.owner)
    fluxo_form = FluxoRegisterForm(request.POST or None)


    return render(request, 'list_fluxo.html',
                  {'fluxos': fluxos, 'fluxo_form': fluxo_form, 'profile': profile})

@csrf_exempt
@login_required
def adicionar_fluxo_ged(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    fluxo_instance = FluxoEmissao()
    fluxo_form = FluxoRegisterForm(request.POST or None, instance=fluxo_instance)

    if request.method == "POST":
        if fluxo_form.is_valid():
            sigla_novo = request.POST.get('sigla_tipo_emissao')
            count = FluxoEmissao.objects.filter(sigla_tipo_emissao=sigla_novo, owner=profile.owner).count()
            if count > 0:
                messages.error(request, 'Sigla já cadastrada!!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            fluxo = fluxo_form.save(commit=False)
            fluxo.owner = profile.owner
            fluxo.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def fluxo_ged_edit_ajax(request, pk):
    fluxo = FluxoEmissao.objects.get(id=pk)

    data = {
        'sigla_tipo_emissao': fluxo.sigla_tipo_emissao,
        'tipo_emissão': fluxo.tipo_emissão,
        'certifica_primeira_emissão': fluxo.certifica_primeira_emissão,
        'cancelado': fluxo.cancelado,
    }

    return JsonResponse(data)




@login_required
def fluxo_ged_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    id = request.POST.get("id_edit")
    fluxo_instance = FluxoEmissao.objects.get(id=id)
    fluxo_form = FluxoRegisterForm(request.POST or None, instance=fluxo_instance)
    if request.method == "POST":

        if fluxo_form.is_valid():
            sigla_edit = request.POST.get('sigla_tipo_emissao')
            count = FluxoEmissao.objects.filter(sigla_tipo_emissao=sigla_edit, owner=profile.owner).count()
            if count > 0:
                registro = FluxoEmissao.objects.get(sigla_tipo_emissao=sigla_edit, owner=profile.owner)
                if fluxo_instance.id == registro.id:
                    pass
                else:
                    messages.error(request, 'Sigla já cadastrada!!')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            fluxo = fluxo_form.save(commit=False)
            try:
                fluxo.save()
            except:
                # messages.error(request, 'Usuário já cadastrado com esse e-mail')

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
@login_required
def fluxo_ged_deletar(request):
    fluxo_ged_id_delet = request.POST.get('id_delet')
    fluxo_ged = FluxoEmissao.objects.get(id=fluxo_ged_id_delet)
    fluxo_ged.delete()
    messages.success(request, "Etapa deletada com sucesso!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
@login_required
def execucao_ld(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)
    fornecedores_owner = Fornecedores.objects.filter(owner=profile.owner)
    if request.method == 'POST':
        form_projeto_ld = LDFormCarga(request.POST or None, fornecedor_queryset=fornecedores_owner)

        if form_projeto_ld.is_valid():
            ld = form_projeto_ld.save(commit=False)
            ld.projeto = projeto
            ld.unidade = projeto.unidade
            ld.owner = projeto.unidade.owner
            ld.profile = profile

            ld.tipo = 'LD'
            ld.save()

            arquivold_file = request.FILES.get('arquivold')
            if arquivold_file != None:
                blob_name = conector_blob(ld, arquivold_file) # função para salvar o arquivo na storage
                ld.arquivold = blob_name

                ld.status = 'Finalizado'
                ld.save()


            run_ld(arquivold_file, projeto_id, ld, request)
            if ld.status == 'ERRO':
                
                projeto = ld.projeto
                usuario = request.user
                profile = Profile.objects.get(user=usuario)

                fornecedores_owner = Fornecedores.objects.filter(owner=profile.owner)

                form_projeto_ged = GEDFormCarga(request.POST or None)
                form_projeto_ld = LDFormCarga(request.POST or None, fornecedor_queryset=fornecedores_owner)

                execucoes = ExecucaoLD.objects.filter(projeto=projeto).order_by('-data_execucao')
                configura_ld_instance = ConfiguraLd.objects.get(projeto=projeto)
                form_configura = ConfiguraLdForm(request.POST or None, instance=configura_ld_instance)
                messages.error(request, "Não foi possível carregar o arquivo! verifique os logs de processamento!")

                contexto = {'projeto': projeto, 'form_configura': form_configura, 'execucoes': execucoes,
                        'form_projeto_ged': form_projeto_ged, 'form_projeto_ld': form_projeto_ld, 'usuario': usuario,
                        'profile': profile}

                return render(request, 'projeto_ged.html', contexto)


            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form_projeto_ld.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required
def download_arquivo(request, id):
    arquivold = get_object_or_404(ExecucaoLD, id=id)
    if not arquivold.arquivold:
        raise Http404

    response = HttpResponse(arquivold.arquivold, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{arquivold.arquivold}"'

    return response
@login_required
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


@csrf_exempt
@login_required
def exportar_log(request, id):

        output = io.BytesIO()

        criar_planilha_log(output, id)

        output.seek(0)

        filename = 'log_processamento.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


@login_required
@csrf_exempt
def configura_ged(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)

    configura_ged_instance = ConfiguraGED.objects.get(projeto=projeto)
    form_configura_ged = ConfiguraGEDForm(request.POST or None, instance=configura_ged_instance)
    if request.method == "POST":
        if form_configura_ged.is_valid():
            form_configura_ged.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required
def execucao_ged(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    if request.method == 'POST':
        form_projeto_ged = GEDFormCarga(request.POST or None)

        if form_projeto_ged.is_valid():
            ged = form_projeto_ged.save(commit=False)
            ged.projeto = projeto
            ged.unidade = projeto.unidade
            ged.owner = projeto.unidade.owner
            ged.profile = profile

            ged.tipo = 'GED'

            arquivo_file = request.FILES.get('arquivold')
            if arquivo_file != None:

                blob_name = conector_blob(ld=ged, arquivo_file=arquivo_file)  # função para salvar o arquivo na storage
                ged.arquivold = blob_name

                ged.status = 'Finalizado'
                ged.save()

            run_ged(arquivo_file, projeto_id, ged, request)
            if ged.status == 'ERRO':
                projeto = ged.projeto
                usuario = request.user
                profile = Profile.objects.get(user=usuario)

                fornecedores_owner = Fornecedores.objects.filter(owner=profile.owner)

                form_projeto_ged = GEDFormCarga(request.POST or None)
                form_projeto_ld = LDFormCarga(request.POST or None, fornecedor_queryset=fornecedores_owner)

                execucoes = ExecucaoLD.objects.filter(projeto=projeto).order_by('-data_execucao')
                configura_ld_instance = ConfiguraLd.objects.get(projeto=projeto)
                form_configura = ConfiguraLdForm(request.POST or None, instance=configura_ld_instance)
                messages.error(request, "Não foi possível carregar o arquivo! verifique os logs de processamento!")

                contexto = {'projeto': projeto, 'form_configura': form_configura, 'execucoes': execucoes,
                            'form_projeto_ged': form_projeto_ged, 'form_projeto_ld': form_projeto_ld,
                            'usuario': usuario,
                            'profile': profile}

                return render(request, 'projeto_detail.html', contexto)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form_projeto_ged.errors)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




@csrf_exempt
@login_required
def list_fluxo_retorno(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    fluxos = FluxoDevolucaoGED.objects.filter(owner=profile.owner)
    fluxo_devolucao_form = FluxoDevolucaoForm(request.POST or None)


    return render(request, 'list_fluxo_ged.html',
                  {'fluxos': fluxos, 'fluxo_devolucao_form': fluxo_devolucao_form, 'profile': profile})


@csrf_exempt
@login_required
def adicionar_fluxo_devolucao_ged(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    fluxo_instance = FluxoDevolucaoGED()
    fluxo_devolucao_form = FluxoDevolucaoForm(request.POST or None, instance=fluxo_instance)

    if request.method == "POST":
        if fluxo_devolucao_form.is_valid():
            sigla_novo = request.POST.get('sigla_devolucao')
            count = FluxoDevolucaoGED.objects.filter(sigla_devolucao=sigla_novo, owner=profile.owner).count()
            if count > 0:
                messages.error(request, 'Sigla já cadastrada!!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            fluxo = fluxo_devolucao_form.save(commit=False)
            fluxo.owner = profile.owner
            fluxo.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def fluxo_ged_devolucao_edit_ajax(request, pk):
    fluxo = FluxoDevolucaoGED.objects.get(id=pk)

    data = {
        'sigla_devolucao': fluxo.sigla_devolucao,
        'certificado': fluxo.certificado,
        'cancelado': fluxo.cancelado,
    }

    return JsonResponse(data)




@login_required
def fluxo_ged_devolucao_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    id = request.POST.get("id_edit")
    fluxo_instance = FluxoDevolucaoGED.objects.get(id=id)
    fluxo_devolucao_form = FluxoDevolucaoForm(request.POST or None, instance=fluxo_instance)
    if request.method == "POST":

        if fluxo_devolucao_form.is_valid():
            sigla_edit = request.POST.get('sigla_devolucao')
            count = FluxoDevolucaoGED.objects.filter(sigla_devolucao=sigla_edit, owner=profile.owner).count()
            if count > 0:
                registro = FluxoDevolucaoGED.objects.get(sigla_devolucao=sigla_edit, owner=profile.owner)
                if fluxo_instance.id == registro.id:
                    pass
                else:
                    messages.error(request, 'Sigla já cadastrada!!')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            fluxo = fluxo_devolucao_form.save(commit=False)
            try:
                fluxo.save()
            except:
                # messages.error(request, 'Usuário já cadastrado com esse e-mail')

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
@login_required
def fluxo_ged_devolucao_deletar(request):
    fluxo_ged_id_delet = request.POST.get('id_delet')
    fluxo_ged = FluxoDevolucaoGED.objects.get(id=fluxo_ged_id_delet)
    fluxo_ged.delete()
    messages.success(request, "Etapa deletada com sucesso!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))