import io
import pyodbc
from sqlalchemy import create_engine
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
from apps.core.conector_blob_arquivos import conector_blob, arquiv_xer_storage, caminho_file
from apps.core.emmanuel.loader import _cronograma, _curva
from apps.cronograma_master.etl_avanco_master import run_avanco_master, run_avanco_master_recurso
from apps.cronograma_master.etl_baseline import run_crono_master_baseline
from apps.cronograma_master.etl_cronograma_master import run_crono_master
#from apps.cronograma_master.etl_xer import run_etl_xer
from apps.cronograma_master.forms import CronogramaMasterFormCarga, ConfiguraCronogramaMasterForm, \
    CronogramaMasterFormCargaXer, CronogramaMasterBaselineFormCarga, CronogramaMasterAvancoFormCarga
from apps.cronograma_master.models import ConfiguraCronogramaMaster, ExecucaoCronoMaster, \
    LogProcessamentoCronogramaMaster, ContainerCronoMaster, ADFContainerCronoMasterCronogramas, TabelaTaskAvancoMaster, \
    TabelaTaskrsrcAvancoMaster
from apps.cronograma_master.planilha_avanco import criar_planilha_avanco, verifica_datas_reprogramadas
from apps.cronogramacontratadas.models import StageCronogramaContratadaAtividade, CronogramaContratada
from apps.projeto.models import Projeto
from apps.usuario.models import Profile
from django.db.models import Max, F
import pandas as pd
from django.db.models import Count
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
            # arquivo_file.seek(0)
            # if arquivo_file.name.endswith('xer'):
            #     with tempfile.NamedTemporaryFile(suffix='.xer',delete=False) as tmp_file:
            #         shutil.copyfileobj(arquivo_file, tmp_file)
            #
            #         tmp_file.flush()
            #         tmp_file.seek(0)


                    #caminho_arquivo_temporario = os.path.join(tempfile.gettempdir(), tmp_file.name)
                    #print(caminho_arquivo_temporario)

                    #run_etl_xer(caminho_arquivo_temporario, projeto, crono, container, request)

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
def execucao_cronograma_master_crono_baseline_xer(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    container_id = request.POST.get("container_id")
    container = ContainerCronoMaster.objects.get(id=container_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)
    execucao_cronograma = ExecucaoCronoMaster.objects.filter(container=container, tipo="BASELINE XER", status="Finalizado").count()
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

            crono.tipo = 'BASELINE XER'

            arquivo_file = request.FILES.get('arquivo')
            if arquivo_file != None:
                blob_name = conector_blob(ld=crono, arquivo_file=arquivo_file)  # função para salvar o arquivo na storage
                crono.arquivo = blob_name


                crono.status = 'Finalizado'
                crono.save()
            # arquivo_file.seek(0)
            # if arquivo_file.name.endswith('xer'):
            #     with tempfile.NamedTemporaryFile(suffix='.xer',delete=False) as tmp_file:
            #         shutil.copyfileobj(arquivo_file, tmp_file)
            #
            #         tmp_file.flush()
            #         tmp_file.seek(0)


                    #caminho_arquivo_temporario = os.path.join(tempfile.gettempdir(), tmp_file.name)
                    #print(caminho_arquivo_temporario)

                    #run_etl_xer(caminho_arquivo_temporario, projeto, crono, container, request)

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
    execucao_baseline = ExecucaoCronoMaster.objects.filter(container=container, tipo="BASELINE CURVA", status="Finalizado").count()
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

            crono.tipo = 'BASELINE CURVA'
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


@csrf_exempt
@login_required
def execuca_deletar(request, id):

    execucao = ExecucaoCronoMaster.objects.get(id=id)
    execucao.delete()
    messages.success(request, "Container deletado com sucesso!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required
def avanco_projeto_crono_master(request, id):
    projeto = Projeto.objects.get(id=id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    tasks = TabelaTaskAvancoMaster.objects.filter(projeto=projeto)
    recursos = TabelaTaskrsrcAvancoMaster.objects.filter(projeto=projeto)
    form = CronogramaMasterAvancoFormCarga(request.POST, request.FILES)


    contexto = {'projeto':projeto, 'usuario':usuario, 'profile':profile, "tasks":tasks, "recursos":recursos, "form":form}


    return render(request, 'avanco_crono_master.html', contexto)



@csrf_exempt
@login_required
def execucao_cronograma_master_avanco(request, id):

    projeto = Projeto.objects.get(id=id)
    projeto_id = projeto.id

    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    tabela_avanco = TabelaTaskAvancoMaster.objects.filter(projeto=projeto)
    tabela_avanco.delete()

    tabela_recurso = TabelaTaskrsrcAvancoMaster.objects.filter(projeto=projeto)
    tabela_recurso.delete()

    if request.method == 'POST':
        form = CronogramaMasterAvancoFormCarga(request.POST, request.FILES)
        if form.is_valid():
            arquivo_file = request.FILES.get('arquivo')
            if arquivo_file != None:

                run_avanco_master(arquivo_file, projeto_id)
                run_avanco_master_recurso(arquivo_file, projeto_id)

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required
def planilha_avanco_projeto(request, id):

    projeto = Projeto.objects.get(id=id)

    tasks = TabelaTaskAvancoMaster.objects.filter(projeto=projeto)
    recursos = TabelaTaskrsrcAvancoMaster.objects.filter(projeto=projeto)

    dados_contatadas = StageCronogramaContratadaAtividade.objects.filter(projeto=projeto)

    contratadas_unicas = dados_contatadas.values('contratada').distinct()

    maior_data_corte_por_contratada = dados_contatadas.values('contratada').annotate(
        max_data_corte=Max('data_corte')
    )

    resultados = []
    for item in maior_data_corte_por_contratada:
        contratada_id = item['contratada']
        max_data_corte = item['max_data_corte']
        contratada = CronogramaContratada.objects.get(id=contratada_id)  # Obtenha o objeto contratada
        # Agora, você pode obter o registro específico com a maior data de corte
        registro_maior_data_corte = StageCronogramaContratadaAtividade.objects.filter(contratada=contratada,
                                                                                      data_corte=max_data_corte)
        resultados.extend(registro_maior_data_corte)

    avancos = {
        'OP_WP': [registro.OP_WP for registro in resultados],
        'avanco': [registro.avanco for registro in resultados],
        'data_inicio_real': [registro.data_inicio_real for registro in resultados],
        'data_fim_real': [registro.data_fim_real for registro in resultados],
        'previsto': [registro.previsto for registro in resultados],
        'actual': [registro.actual for registro in resultados],
    }

    avancos = pd.DataFrame(avancos)

    output = io.BytesIO()

    criar_planilha_avanco(output, tasks, recursos, avancos)

    output.seek(0)

    filename = 'planilha_avanco.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response






def executar_avanco_container_maste(request, id):
    container = ContainerCronoMaster.objects.get(id=id)
    execucoes = ExecucaoCronoMaster.objects.filter(container=container)

    tipos_desejados = ["BASELINE CURVA", "BASELINE XER", "CURVA", "CRONOGRAMA"]
    tipos_encontrados = execucoes.values('tipo').annotate(total=Count('tipo'))
    tipos_encontrados_dict = {item['tipo']: item['total'] for item in tipos_encontrados}
    todos_os_tipos_encontrados = all(tipo in tipos_encontrados_dict and tipos_encontrados_dict[tipo] == 1 for tipo in tipos_desejados)

    if todos_os_tipos_encontrados:

        conn_str = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=onca-puma.database.windows.net;"
            "Database=DB_Verum_IPE;"
            "uid=emmanuelsantana;"
            "pwd=Recife@2023"
        )
        cnxn = pyodbc.connect(conn_str)
        engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn_str))


        for execucao in execucoes:
            if execucao.tipo == "BASELINE CURVA":
                bl_path_curva = caminho_file(request, execucao.arquivo.name)
            elif execucao.tipo == "BASELINE XER":
                bl_path_xer = caminho_file(request, execucao.arquivo.name)
                print()



        for execucao in execucoes:
            if execucao.arquivo.name.endswith('xlsx') and execucao.tipo == "CURVA":
                _curva(file_path=caminho_file(request, execucao.arquivo.name), execucao_id=container.id, bl_path=bl_path_curva, engine=engine, cnxn=cnxn, projeto_id=container.projeto.id)

            if execucao.arquivo.name.endswith('xer') and execucao.tipo == "CRONOGRAMA":
                _cronograma(file_path=caminho_file(request, execucao.arquivo.name), execucao_id=container.id, bl_path_xer=bl_path_xer, engine=engine, cnxn=cnxn, projeto_id=container.projeto.id)

        container.status = "Finalizado"
        container.save()
        cnxn.close()
        engine.dispose()

    else:
        messages.error(request, "Para executar a carga você deve ter os arquivos carregados no container!")


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





def verifica_datas_master(request, id):
    projeto = Projeto.objects.get(id=id)
    tasks = TabelaTaskAvancoMaster.objects.filter(projeto=projeto)

    dados_contatadas = StageCronogramaContratadaAtividade.objects.filter(projeto=projeto)

    contratadas_unicas = dados_contatadas.values('contratada').distinct()

    maior_data_corte_por_contratada = dados_contatadas.values('contratada').annotate(
        max_data_corte=Max('data_corte')
    )

    resultados = []
    for item in maior_data_corte_por_contratada:
        contratada_id = item['contratada']
        max_data_corte = item['max_data_corte']
        contratada = CronogramaContratada.objects.get(id=contratada_id)  # Obtenha o objeto contratada
        # Agora, você pode obter o registro específico com a maior data de corte
        registro_maior_data_corte = StageCronogramaContratadaAtividade.objects.filter(contratada=contratada,
                                                                                      data_corte=max_data_corte)
        resultados.extend(registro_maior_data_corte)

    avancos = {
        'OP_WP': [registro.OP_WP for registro in resultados],
        'avanco': [registro.avanco for registro in resultados],
        'data_inicio_real': [registro.data_inicio_real for registro in resultados],
        'data_fim_real': [registro.data_fim_real for registro in resultados],
        'data_inicio_reprogramada': [registro.data_inicio_reprogramado for registro in resultados],
        'data_fim_reprogramada': [registro.data_fim_reprogramado for registro in resultados],
        'previsto': [registro.previsto for registro in resultados],
        'actual': [registro.actual for registro in resultados],
    }

    output = io.BytesIO()
    avancos = pd.DataFrame(avancos)



    df = pd.DataFrame(columns=['OP_atividade', 'task_code', 'data', 'valor CR contratada', 'valor CR master'])
    df = verifica_datas_reprogramadas(avancos, tasks, df)
    df.to_excel(output)
    df.to_excel("verificacao.xlsx")
    output.seek(0)

    filename = 'verifição_datas_master.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

