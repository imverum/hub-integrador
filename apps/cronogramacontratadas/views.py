import shutil

from django.shortcuts import render
import datetime
from django.db.models import Max
from apps.core.conector_blob_arquivos import conector_blob
from apps.cronograma_master.models import TabelaTaskAvancoMaster
from apps.cronogramacontratadas.carga_app import carga_app, etl_pandas_xer, carga_dados_banco
from apps.cronogramacontratadas.etl_cronograma_contratada_atividades import run_crono_contratada_atividades
from apps.cronogramacontratadas.forms import CronogramaCrontratadaAddForm, CronogramaContratadaFormCarga
from apps.cronogramacontratadas.models import CronogramaContratada, ExecucaoCronoContratadas, \
    StageCronogramaContratadaAtividade
from apps.cronogramacontratadas.validacao_cronograma_contratada import cria_planilha_validacao
from apps.fornecedores.models import Fornecedores
from apps.projeto.models import Projeto
from apps.usuario.models import Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib import messages
import io
from django.http import HttpResponse
import tempfile
import os
# Create your views here.
@csrf_exempt
@login_required
def list_cronograma_contratada(request, id):
    projeto = Projeto.objects.get(id=id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    contratada_queryset = Fornecedores.objects.filter(owner=profile.owner)

    form = CronogramaCrontratadaAddForm(request.POST or None, contratada_queryset=contratada_queryset)

    cronogramas = CronogramaContratada.objects.filter(projeto=projeto)
    contexto = {'projeto':projeto,'usuario':usuario, 'profile':profile, 'cronogramas':cronogramas, "form":form, "contratada_queryset":contratada_queryset}



    return render(request, 'contratadas_cronograma.html', contexto)

@csrf_exempt
@login_required
def register_cronograma_contratada(request, id):
    projeto = Projeto.objects.get(id=id)
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        instance = CronogramaContratada()
        form = CronogramaCrontratadaAddForm(request.POST or None)

        if form.is_valid():
            new = form.save(commit=False)
            new.owner = profile.owner
            new.profile = profile
            new.projeto = projeto
            new.unidade = projeto.unidade
            new.data_ciacao = datetime.date.today()

            new.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@csrf_exempt
@login_required
def processo_documento_deletar(request):
    id = request.POST.get("id_delet")
    user = request.user
    profile_edicao = Profile.objects.get(user=user)
    cronograma = CronogramaContratada.objects.get(id=id)

    try:
        cronograma.delete()
    except:
        messages.success(request, "Esse Cronograma não pode ser deletada, pois ainda existem informações cadastradas para ele!")

    messages.success(request, "Cronograma deletado com sucesso!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required
def list_cargas_cronograma_contratada(request, id):
    contratada = CronogramaContratada.objects.get(id=id)
    projeto = contratada.projeto
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    form = CronogramaContratadaFormCarga(request.POST or None)

    cronogramas = ExecucaoCronoContratadas.objects.filter(contratada=contratada)
    contexto = {'projeto':projeto,'usuario':usuario, 'profile':profile, 'cronogramas':cronogramas, "form":form, "contratada":contratada}

    return render(request, 'cronograma_contratada_carga.html', contexto)


@csrf_exempt
@login_required
def execucao_cronograma_contratada_atividades(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    contratada_id = request.POST.get("contratada_id")
    contratada = CronogramaContratada.objects.get(id=contratada_id)
    contratada_id = contratada.id

    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    execucoes_contratada = ExecucaoCronoContratadas.objects.filter(contratada=contratada)
    maior_data_corte = execucoes_contratada.aggregate(Max('data_corte'))

    print(maior_data_corte)



    if request.method == 'POST':
        form_projeto_crono_contratada_atividade = CronogramaContratadaFormCarga(request.POST, request.FILES)

        if form_projeto_crono_contratada_atividade.is_valid():
            crono = form_projeto_crono_contratada_atividade.save(commit=False)

            if ExecucaoCronoContratadas.objects.filter(contratada=contratada, data_corte=crono.data_corte).exists():
                messages.error(request, 'Carga já cadastrada para a Data Corte')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if maior_data_corte["data_corte__max"] == None:
                pass
            else:
                if maior_data_corte["data_corte__max"] > crono.data_corte:
                    messages.error(request, f'Para atualizar os dados do seu cronograma você precisa salvar uma atualização com uma data corte maior do que {maior_data_corte["data_corte__max"]}')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


            crono.projeto = projeto
            crono.unidade = projeto.unidade
            crono.owner = projeto.unidade.owner
            crono.profile = profile
            crono.contratada = contratada
            crono.arquivo = None
            crono.save()

            arquivo_file = request.FILES.get('arquivo')
            if arquivo_file != None:
                pass
                #blob_name = conector_blob(ld=crono, arquivo_file=arquivo_file)  # função para salvar o arquivo na storage
                #crono.arquivo = blob_name
                #crono.save()

            data_corte = crono.data_corte
            op_wp = request.POST.get("codexer")
            run_crono_contratada_atividades(arquivo_file, projeto_id, crono, data_corte, contratada_id, op_wp)
            if crono.status == 'ERRO':

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@csrf_exempt
@login_required
def execucao_cronograma_contratada_deletar(request):
    id = request.POST.get("id_delet")
    user = request.user
    profile_edicao = Profile.objects.get(user=user)
    cronograma = ExecucaoCronoContratadas.objects.get(id=id)

    try:
        cronograma.delete()
    except:
        messages.success(request, "Esse Cronograma não pode ser deletada, pois ainda existem informações cadastradas para ele!")

    messages.success(request, "Cronograma deletado com sucesso!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@csrf_exempt
@login_required
def validacao_cronograma_contratdas(request, data_corte, contratada):
    contratada = CronogramaContratada.objects.get(id=contratada)
    atividades = StageCronogramaContratadaAtividade.objects.filter(data_corte=data_corte,contratada=contratada )
    print(atividades)
    projeto = atividades.first().projeto if atividades.exists() else None
    ops_master = TabelaTaskAvancoMaster.objects.filter(projeto=projeto).values_list('op_cwp', flat=True).distinct()


    output = io.BytesIO()

    cria_planilha_validacao(output, ops_master, atividades)

    output.seek(0)

    filename = 'logs_cronograma.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@csrf_exempt
def carga_mip(request):
    if request.method == 'POST':
        arquivo_file = request.FILES.get('xer_file')
        if arquivo_file != None:
            arquivo_file.seek(0)
            if arquivo_file.name.endswith('xer'):
                 with tempfile.NamedTemporaryFile(suffix='.xer',delete=False) as tmp_file:
                    shutil.copyfileobj(arquivo_file, tmp_file)
                    tmp_file.flush()
                    tmp_file.seek(0)

            caminho_arquivo_temporario = os.path.join(tempfile.gettempdir(), tmp_file.name)
            print(caminho_arquivo_temporario)

            df_carga = carga_app(caminho_arquivo_temporario)
            df_carga = etl_pandas_xer(df_carga)
            carga_dados_banco(df_carga)

        return render(request, 'carga_mip.html')

    else:

        return render(request,'carga_mip.html')


