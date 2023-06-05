import io
import shutil
import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import tempfile
import datetime
from apps.core.acesso_logs import criar_planilha_log_geral
from apps.core.conector_blob_arquivos import conector_blob, arquiv_xer_storage
from apps.cronograma_master.etl_baseline import run_crono_master_baseline
from apps.cronograma_master.etl_cronograma_master import run_crono_master
from apps.cronograma_master.etl_xer import run_etl_xer
from apps.cronograma_master.forms import CronogramaMasterFormCarga, ConfiguraCronogramaMasterForm, \
    CronogramaMasterFormCargaXer, CronogramaMasterBaselineFormCarga
from apps.cronograma_master.models import ConfiguraCronogramaMaster, ExecucaoCronoMaster, \
    LogProcessamentoCronogramaMaster, ContainerCronoMaster, ADFContainerCronoMasterCronogramas
from apps.projeto.models import Projeto
from apps.usuario.models import Profile


@csrf_exempt
@login_required
def execucao_cronograma_master(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    container_id = request.POST.get("container_id")
    container = ContainerCronoMaster.objects.get(id=container_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)
    execucao_curva = ExecucaoCronoMaster.objects.filter(container=container, tipo="CURVA", status="Finalizado").count()
    if execucao_curva > 0:
        messages.error(request, "Você só pode ter um arquivo de curva finalizado salvo por container!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        form_projeto_crono_master = CronogramaMasterFormCarga(request.POST, request.FILES)

        if form_projeto_crono_master.is_valid():
            crono = form_projeto_crono_master.save(commit=False)
            crono.projeto = projeto
            crono.unidade = projeto.unidade
            crono.owner = projeto.unidade.owner
            crono.profile = profile
            crono.container = container
            crono.inicio_preprocessament = datetime.datetime.now().time()
            crono.arquivo = None
            crono.save()

            crono.tipo = 'CURVA'
            crono.save()

            arquivo_file = request.FILES.get('arquivo')
            if arquivo_file != None:
                blob_name = conector_blob(ld=crono, arquivo_file=arquivo_file)  # função para salvar o arquivo na storage
                crono.arquivo = blob_name

                crono.status = 'Finalizado'

                crono.save()

            run_crono_master(arquivo_file, projeto_id, crono, request, container)
            if crono.status == 'ERRO':
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            container.status = "Em Andamento"
            container.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form_projeto_crono_master.errors)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@csrf_exempt
@login_required
def execucao_cronograma_master_crono(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    container_id = request.POST.get("container_id")
    container = ContainerCronoMaster.objects.get(id=container_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)
    execucao_cronograma = ExecucaoCronoMaster.objects.filter(container=container, tipo="CRONOGRAMA", status="Finalizado").count()
    if execucao_cronograma > 0:
        messages.error(request, "Você só pode ter um arquivo cronograma finalizado salvo por container!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        form_projeto_crono_master = CronogramaMasterFormCarga(request.POST, request.FILES)

        if form_projeto_crono_master.is_valid():
            crono = form_projeto_crono_master.save(commit=False)
            crono.projeto = projeto
            crono.unidade = projeto.unidade
            crono.owner = projeto.unidade.owner
            crono.profile = profile
            crono.container = container
            crono.arquivo = None
            crono.save()

            crono.tipo = 'CRONOGRAMA'

            arquivo_file = request.FILES.get('arquivo')
            if arquivo_file != None:
                blob_name = conector_blob(ld=crono, arquivo_file=arquivo_file)  # função para salvar o arquivo na storage
                crono.arquivo = blob_name


                crono.status = 'Finalizado'
                crono.save()
            arquivo_file.seek(0)
            if arquivo_file.name.endswith('xer'):
                with tempfile.NamedTemporaryFile(suffix='.xer',delete=False) as tmp_file:
                    shutil.copyfileobj(arquivo_file, tmp_file)

                    tmp_file.flush()
                    tmp_file.seek(0)


                    caminho_arquivo_temporario = os.path.join(tempfile.gettempdir(), tmp_file.name)
                    print(caminho_arquivo_temporario)

                    run_etl_xer(caminho_arquivo_temporario, projeto, crono, container, request)

            if crono.status == 'ERRO':
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            container.status = "Em Andamento"
            container.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form_projeto_crono_master.errors)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





@csrf_exempt
@login_required
def exportar_log_crono_master(request, id):

        output = io.BytesIO()
        execucao = ExecucaoCronoMaster.objects.get(id=id)
        logs = LogProcessamentoCronogramaMaster.objects.filter(execucao=execucao)

        criar_planilha_log_geral(output, logs)

        output.seek(0)

        filename = 'log_processamento.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response

@csrf_exempt
@login_required
def execucao_cronograma_master_baseline(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    container_id = request.POST.get("container_id")
    container = ContainerCronoMaster.objects.get(id=container_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)
    execucao_baseline = ExecucaoCronoMaster.objects.filter(container=container, tipo="BASELINE", status="Finalizado").count()
    if execucao_baseline >0:
        messages.error(request,"Você só pode ter um arquivo Baseline finalizado salvo por container!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    if request.method == 'POST':
        form_projeto_crono_master_baseline = CronogramaMasterBaselineFormCarga(request.POST, request.FILES)

        if form_projeto_crono_master_baseline.is_valid():
            crono = form_projeto_crono_master_baseline.save(commit=False)
            crono.projeto = projeto
            crono.unidade = projeto.unidade
            crono.owner = projeto.unidade.owner
            crono.profile = profile
            crono.container = container
            crono.arquivo = None
            crono.save()

            crono.tipo = 'BASELINE'
            crono.save()
            container.status = "Em Andamento"
            container.save()

            arquivo_file = request.FILES.get('arquivo')
            if arquivo_file != None:
                blob_name = conector_blob(ld=crono, arquivo_file=arquivo_file)  # função para salvar o arquivo na storage
                crono.arquivo = blob_name

                crono.status = 'Finalizado'

                crono.save()

            run_crono_master_baseline(arquivo_file, projeto_id, crono, request, container)
            if crono.status == 'ERRO':


                form_projeto_crono_master = CronogramaMasterFormCarga(request.POST or None)

                configura_crono_master_instance = ConfiguraCronogramaMaster.objects.get(projeto=projeto)
                form_configura = ConfiguraCronogramaMasterForm(request.POST or None,
                                                               instance=configura_crono_master_instance)

                execucoes = ExecucaoCronoMaster.objects.filter(projeto=projeto).order_by('-data_execucao')
                paginator = Paginator(execucoes, 10)
                page = request.GET.get("page")
                page_obj = paginator.get_page(page)
                try:
                    execucoes_page = paginator.page(page)
                except PageNotAnInteger:
                    execucoes_page = paginator.page(1)
                except EmptyPage:
                    execucoes_page = paginator.page(paginator.num_pages)

                contexto = {'projeto': projeto, 'form_configura': form_configura, 'execucoes_page': execucoes_page,
                            'page_obj': page_obj, 'usuario': usuario, 'profile': profile,
                            'form_projeto_crono_master': form_projeto_crono_master}

                return render(request, 'projeto_crono_master.html', contexto)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form_projeto_crono_master_baseline.errors)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@csrf_exempt
@login_required
def container_projeto_crono_master(request, id):
    projeto = Projeto.objects.get(id=id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    container = ContainerCronoMaster.objects.filter(projeto=projeto).order_by('-data_ciacao')
    paginator = Paginator(container, 10)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    try:
        container_page = paginator.page(page)
    except PageNotAnInteger:
        container_page = paginator.page(1)
    except EmptyPage:
        container_page = paginator.page(paginator.num_pages)

    contexto = {'projeto':projeto, 'container_page':container_page, 'page_obj':page_obj,'usuario':usuario, 'profile':profile}


    return render(request, 'container_crono_master.html', contexto)


@csrf_exempt
@login_required
def criar_container_projeto_crono_master(request, id):
    projeto = Projeto.objects.get(id=id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)
    container_existe = ContainerCronoMaster.objects.filter(projeto=projeto,status='Aguardando Carga').exists()
    container_existee = ContainerCronoMaster.objects.filter(projeto=projeto,status='Em Andamento').exists()

    if container_existe or container_existee:
        messages.error(request, "Não foi possível criar o container! Você ainda tem container em aberto!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



    nome = f"Container_{projeto.projeto}"
    container = ContainerCronoMaster.objects.create(
        owner = profile.owner,
        profile = profile,
        unidade = projeto.unidade,
        projeto = projeto,
        nome= nome,
        status="Aguardando Carga"
    )

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required
def projeto_crono_master(request, id):
    container = ContainerCronoMaster.objects.get(id=id)
    projeto = container.projeto
    usuario = request.user
    profile = Profile.objects.get(user=usuario)


    form_projeto_crono_master = CronogramaMasterFormCarga(request.POST or None)

    form_projeto_crono_master_baseline = CronogramaMasterBaselineFormCarga(request.POST or None)

    configura_crono_master_instance = ConfiguraCronogramaMaster.objects.get(projeto=projeto)
    form_configura = ConfiguraCronogramaMasterForm(request.POST or None, instance=configura_crono_master_instance)


    execucoes = ExecucaoCronoMaster.objects.filter(container=container).order_by('-data_execucao')
    paginator = Paginator(execucoes, 10)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    try:
        execucoes_page = paginator.page(page)
    except PageNotAnInteger:
        execucoes_page = paginator.page(1)
    except EmptyPage:
        execucoes_page = paginator.page(paginator.num_pages)

    contexto = {'form_projeto_crono_master_baseline':form_projeto_crono_master_baseline,'projeto':projeto,'container':container ,'form_configura':form_configura, 'execucoes_page':execucoes_page, 'page_obj':page_obj,'usuario':usuario, 'profile':profile, 'form_projeto_crono_master':form_projeto_crono_master}


    return render(request, 'projeto_crono_master.html', contexto)


def execucao_container_crono_master(request, id):
    container = ContainerCronoMaster.objects.get(id=id)
    projeto_id= request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    execucao_cronograma = ExecucaoCronoMaster.objects.filter(container=container, tipo="CRONOGRAMA", status="Finalizado").count()
    execucao_curva = ExecucaoCronoMaster.objects.filter(container=container, tipo="CURVA", status="Finalizado").count()

    if execucao_cronograma >0 and execucao_curva>0:

        carga = ADFContainerCronoMasterCronogramas.objects.create(
            container=container,
            status_execucao_adf="Pendente",
            projeto=projeto
        )
        container.status = "Finalizado"
        container.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "Para solicitar a execução do container você precisa ter uma curva e um cronograma carregados!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@csrf_exempt
@login_required
def container_deletar(request, id):

    container = ContainerCronoMaster.objects.get(id=id)
    container.delete()
    messages.success(request, "Container deletado com sucesso!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))