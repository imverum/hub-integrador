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

from apps.core.acesso_logs import criar_planilha_log_geral
from apps.core.conector_blob_arquivos import conector_blob, arquiv_xer_storage
from apps.cronograma_master.etl_cronograma_master import run_crono_master
from apps.cronograma_master.etl_xer import run_etl_xer
from apps.cronograma_master.forms import CronogramaMasterFormCarga, ConfiguraCronogramaMasterForm, \
    CronogramaMasterFormCargaXer
from apps.cronograma_master.models import ConfiguraCronogramaMaster, ExecucaoCronoMaster, \
    LogProcessamentoCronogramaMaster
from apps.projeto.models import Projeto
from apps.usuario.models import Profile


@csrf_exempt
@login_required
def execucao_cronograma_master(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    if request.method == 'POST':
        form_projeto_crono_master = CronogramaMasterFormCarga(request.POST, request.FILES)

        if form_projeto_crono_master.is_valid():
            crono = form_projeto_crono_master.save(commit=False)
            crono.projeto = projeto
            crono.unidade = projeto.unidade
            crono.owner = projeto.unidade.owner
            crono.profile = profile
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

            run_crono_master(arquivo_file, projeto_id, crono, request)
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
            print(form_projeto_crono_master.errors)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@csrf_exempt
@login_required
def execucao_cronograma_master_crono(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    if request.method == 'POST':
        form_projeto_crono_master = CronogramaMasterFormCarga(request.POST, request.FILES)

        if form_projeto_crono_master.is_valid():
            crono = form_projeto_crono_master.save(commit=False)
            crono.projeto = projeto
            crono.unidade = projeto.unidade
            crono.owner = projeto.unidade.owner
            crono.profile = profile
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

                    run_etl_xer(caminho_arquivo_temporario, projeto, crono, request)
                    

            if crono.status == 'ERRO':

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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