from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.core.conector_blob_arquivos import conector_blob
from apps.master_index.etl_cwa import run_cwa
from apps.master_index.etl_pacotes import run_pacotes
from apps.master_index.forms import PacotesFormCarga, ConfiguraPacotesForm, ConfiguraCWAForm, CWAFormCarga
from apps.master_index.models import ConfiguraMasterIndexPacotes, ConfiguraMasterIndexCWA, ExecucaoMasterIndex
from apps.projeto.models import Projeto
from apps.usuario.models import Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse

@csrf_exempt
@login_required
def execucao_master_index_pacotes(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    if request.method == 'POST':
        form_projeto_pacotes = PacotesFormCarga(request.POST, request.FILES)

        if form_projeto_pacotes.is_valid():
            pacotes = form_projeto_pacotes.save(commit=False)
            pacotes.projeto = projeto
            pacotes.unidade = projeto.unidade
            pacotes.owner = projeto.unidade.owner
            pacotes.profile = profile
            pacotes.arquivo = None

            pacotes.tipo = 'Pacotes'
            pacotes.save()

            arquivo_file = request.FILES.get('arquivo')
            if arquivo_file != None:
                blob_name = conector_blob(ld=pacotes, arquivo_file=arquivo_file)  # função para salvar o arquivo na storage
                pacotes.arquivo = blob_name

                pacotes.status = 'Finalizado'
                pacotes.save()

            run_pacotes(arquivo_file, projeto_id, pacotes, request)
            if pacotes.status == 'ERRO':
                projeto = pacotes.projeto
                usuario = request.user
                profile = Profile.objects.get(user=usuario)
                messages.error(request, "Não foi possível carregar o arquivo! verifique os logs de processamento!")
                form_projeto_cwa = CWAFormCarga(request.POST or None)
                form_projeto_pacotes = PacotesFormCarga(request.POST or None)

                configura_cwa_instance = ConfiguraMasterIndexCWA.objects.get(projeto=projeto)
                form_configura_cwa = ConfiguraCWAForm(request.POST or None, instance=configura_cwa_instance)

                configura_pacotes_instance = ConfiguraMasterIndexPacotes.objects.get(projeto=projeto)
                form_configura_pacotes = ConfiguraPacotesForm(request.POST or None, instance=configura_pacotes_instance)

                execucoes = ExecucaoMasterIndex.objects.filter(projeto=projeto).order_by('-data_execucao')
                paginator = Paginator(execucoes, 10)
                page = request.GET.get("page")
                page_obj = paginator.get_page(page)
                try:
                    execucoes_page = paginator.page(page)
                except PageNotAnInteger:
                    execucoes_page = paginator.page(1)
                except EmptyPage:
                    execucoes_page = paginator.page(paginator.num_pages)

                contexto = {'form_configura_cwa': form_configura_cwa, 'projeto': projeto,
                            'form_configura_pacotes': form_configura_pacotes, 'execucoes_page': execucoes_page,
                            'page_obj': page_obj, 'form_projeto_cwa': form_projeto_cwa,
                            'form_projeto_pacotes': form_projeto_pacotes, 'usuario': usuario, 'profile': profile}

                return render(request, 'projeto_master_index.html', contexto)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form_projeto_pacotes.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required
def execucao_master_index_cwa(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    if request.method == 'POST':
        form_projeto_cwa = CWAFormCarga(request.POST, request.FILES)

        if form_projeto_cwa.is_valid():
            cwa = form_projeto_cwa.save(commit=False)
            cwa.projeto = projeto
            cwa.unidade = projeto.unidade
            cwa.owner = projeto.unidade.owner
            cwa.profile = profile
            cwa.arquivo = None

            cwa.tipo = 'CWA'
            cwa.save()

            arquivo_file = request.FILES.get('arquivo')
            if arquivo_file != None:

                blob_name = conector_blob(ld=cwa, arquivo_file=arquivo_file)  # função para salvar o arquivo na storage
                cwa.arquivo = blob_name

                cwa.status = 'Finalizado'
                cwa.save()

            run_cwa(arquivo_file, projeto_id, cwa, request)
            if cwa.status == 'ERRO':
                projeto = cwa.projeto
                usuario = request.user
                profile = Profile.objects.get(user=usuario)
                messages.error(request, "Não foi possível carregar o arquivo! verifique os logs de processamento!")
                form_projeto_cwa = CWAFormCarga(request.POST or None)
                form_projeto_pacotes = PacotesFormCarga(request.POST or None)

                configura_cwa_instance = ConfiguraMasterIndexCWA.objects.get(projeto=projeto)
                form_configura_cwa = ConfiguraCWAForm(request.POST or None, instance=configura_cwa_instance)

                configura_pacotes_instance = ConfiguraMasterIndexPacotes.objects.get(projeto=projeto)
                form_configura_pacotes = ConfiguraPacotesForm(request.POST or None, instance=configura_pacotes_instance)

                execucoes = ExecucaoMasterIndex.objects.filter(projeto=projeto).order_by('-data_execucao')
                paginator = Paginator(execucoes, 10)
                page = request.GET.get("page")
                page_obj = paginator.get_page(page)
                try:
                    execucoes_page = paginator.page(page)
                except PageNotAnInteger:
                    execucoes_page = paginator.page(1)
                except EmptyPage:
                    execucoes_page = paginator.page(paginator.num_pages)

                contexto = {'form_configura_cwa': form_configura_cwa, 'projeto': projeto,
                            'form_configura_pacotes': form_configura_pacotes, 'execucoes_page': execucoes_page,
                            'page_obj': page_obj, 'form_projeto_cwa': form_projeto_cwa,
                            'form_projeto_pacotes': form_projeto_pacotes, 'usuario': usuario, 'profile': profile}

                return render(request, 'projeto_master_index.html', contexto)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form_projeto_cwa.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))