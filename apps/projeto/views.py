from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from apps.core.models import Unidade
from apps.cronograma_master.forms import CronogramaMasterFormCarga, ConfiguraCronogramaMasterForm, \
    CronogramaMasterFormCargaXer
from apps.cronograma_master.models import ConfiguraCronogramaMaster, ExecucaoCronoMaster
from apps.fornecedores.models import Fornecedores
from apps.ged.forms import LDFormCarga, ConfiguraLdForm, ConfiguraGEDForm, GEDFormCarga
from apps.ged.models import ExecucaoLD, ConfiguraLd, ConfiguraGED
from apps.master_index.forms import ConfiguraCWAForm, ConfiguraPacotesForm, CWAFormCarga, PacotesFormCarga
from apps.master_index.models import ConfiguraMasterIndexCWA, ConfiguraMasterIndexPacotes, ExecucaoMasterIndex
from apps.projeto.forms import ProjetoFormAdd
from apps.projeto.models import Projeto, Usuario_Projeto
from apps.usuario.models import Profile
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@csrf_exempt
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
             data_emissão_inicial_prevista='TÉRMINO LINHA DE BASE',
             paginas='PÁGINAS',
             a1_equivalente='A1 EQ.',
             tipo_emissao='TIPO EMISSÃO',
             planilha='ld',
             linha='3',
             coluna='1',
            )

            projeto_ged = ConfiguraGED.objects.create(
                owner=profile.owner,
                unidade=unidade,
                projeto=projeto,
                documento='Numero_Documento',
                revisao='Revisão',
                tipo_documento='CODIGOS_CLASSE_Descricao',
                disciplina='NOME_DISCIPLINA',
                titulo_1='Titulo_1',
                titulo_2='Titulo_2',
                empresa='Nome_Fornecedor',
                numero_contratada='Numero_Fornecedor',
                status_ged='State',
                data_atualizacao='Updated',
                grd_recebimento='Número GRD Entrada',
                data_grd_recebimento='Data GRD Entrada',
                data_analise='Data Análise',
                resultado_analise='Motivo Emissão',
                formato='Formato_Documento',
                work_package_area='Codigo CWA',
                work_package='Codigo Wp',
                tipo_emissao='Codigo_Tipo_Emissao',
                atual_responsavel='Atual Responsável',
                planilha='Relatorio Geral',
                linha='1',
                coluna='0',
            )

            projeto_crono_master = ConfiguraCronogramaMaster.objects.create(
                owner=profile.owner,
                unidade=unidade,
                projeto=projeto,
                activity_id= 'Activity ID',
                resource_name= 'Resource Name',
                resource_type= 'Resource Type',
                spreadsheet_field= 'Spreadsheet Field',
                planilha='Curva',
                linha='0',
                coluna='0',
            )

            projeto_master_index_cwa = ConfiguraMasterIndexCWA.objects.create(
                owner=profile.owner,
                unidade=unidade,
                projeto=projeto,

                codigo_do_projeto='Código do Projeto',
                codigo_cwa='Código CWA',
                descricao='Descrição',
                coordenadas='Cordenadas',
                nivel_do_solo='Nível do Solo',
                planilha='CWA',
                linha='0',
                coluna='0',
            )

            projeto_master_index_pacotes = ConfiguraMasterIndexPacotes.objects.create(
                owner=profile.owner,
                unidade=unidade,
                projeto=projeto,

                codigo_do_projeto='Codigo do Projeto',
                codigo_do_pacote='Código do Pacote',
                descricao='Descrição',
                contrato='Contrato',
                cwa='CWA',
                cwp='CWP',
                subarea='SubArea',
                disciplina='Disciplina',
                subdisciplina='Subdiciplina',
                tipo='Tipo',
                status='Status',
                custo='Custo',
                responsavel='Responsável',
                horas_estimadas='Horas Estimada',

                planilha='Template Pacotes',
                linha='0',
                coluna='0',
            )

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
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
@csrf_exempt
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
    try:
        projeto.delete()
        messages.success(request, "Projeto deletado com sucesso!")
    except:
        messages.success(request, "Esse projeto já tem execuções salvas na base e não pode ser deletado! Para excluir esse projeto entre em contato com o administrador do sistema")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required
def projeto_home(request, id):
    projeto = Projeto.objects.get(id=id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)


    contexto = {'projeto':projeto, 'usuario':usuario, 'profile':profile}


    return render(request, 'projeto_home.html', contexto)


@csrf_exempt
@login_required
def projeto_ged(request, id):
    projeto = Projeto.objects.get(id=id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    fornecedores_owner = Fornecedores.objects.filter(owner=profile.owner)

    form_projeto_ged = GEDFormCarga(request.POST or None)
    form_projeto_ld = LDFormCarga(request.POST or None, fornecedor_queryset=fornecedores_owner)


    configura_ld_instance = ConfiguraLd.objects.get(projeto=projeto)
    form_configura = ConfiguraLdForm(request.POST or None, instance=configura_ld_instance)

    configura_ged_instance = ConfiguraGED.objects.get(projeto=projeto)
    form_configura_ged = ConfiguraGEDForm(request.POST or None, instance=configura_ged_instance)

    execucoes = ExecucaoLD.objects.filter(projeto=projeto).order_by('-data_execucao')
    paginator = Paginator(execucoes, 10)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    try:
        execucoes_page = paginator.page(page)
    except PageNotAnInteger:
        execucoes_page = paginator.page(1)
    except EmptyPage:
        execucoes_page = paginator.page(paginator.num_pages)

    contexto = {'form_configura_ged':form_configura_ged, 'projeto':projeto, 'form_configura':form_configura, 'execucoes_page':execucoes_page, 'page_obj':page_obj, 'form_projeto_ged':form_projeto_ged,'form_projeto_ld':form_projeto_ld ,'usuario':usuario, 'profile':profile}


    return render(request, 'projeto_ged.html', contexto)





@csrf_exempt
@login_required
def projeto_crono_master(request, id):
    projeto = Projeto.objects.get(id=id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)


    form_projeto_crono_master = CronogramaMasterFormCarga(request.POST or None)
    form_projeto_crono_master_xer = CronogramaMasterFormCargaXer(request.POST or None)


    configura_crono_master_instance = ConfiguraCronogramaMaster.objects.get(projeto=projeto)
    form_configura = ConfiguraCronogramaMasterForm(request.POST or None, instance=configura_crono_master_instance)


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

    contexto = {'form_projeto_crono_master_xer':form_projeto_crono_master_xer,'projeto':projeto, 'form_configura':form_configura, 'execucoes_page':execucoes_page, 'page_obj':page_obj,'usuario':usuario, 'profile':profile, 'form_projeto_crono_master':form_projeto_crono_master}


    return render(request, 'projeto_crono_master.html', contexto)


@csrf_exempt
@login_required
def projeto_master_index(request, id):
    projeto = Projeto.objects.get(id=id)
    usuario = request.user
    profile = Profile.objects.get(user=usuario)



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

    contexto = {'form_configura_cwa':form_configura_cwa, 'projeto':projeto, 'form_configura_pacotes':form_configura_pacotes, 'execucoes_page':execucoes_page, 'page_obj':page_obj, 'form_projeto_cwa':form_projeto_cwa,'form_projeto_pacotes':form_projeto_pacotes ,'usuario':usuario, 'profile':profile}


    return render(request, 'projeto_master_index.html', contexto)