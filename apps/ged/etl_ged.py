import pandas as pd

from apps.core.tratar_datas import tratar_data
from apps.ged.models import StageLd, FluxoEmissao, ConfiguraLd, lod_processamento, ExecucaoLD, ConfiguraGED, StageGED
from datetime import datetime
from apps.projeto.models import Projeto
import xlsxwriter as xls
import xlsxwriter.utility as xl_util

def run_ged(arquivold_file, projeto_id, ged, request):

    projeto = Projeto.objects.get(id=projeto_id)
    configuracoes = ConfiguraGED.objects.filter(projeto=projeto).values().first()
    print(configuracoes)

    sheet_names = pd.ExcelFile(arquivold_file)
    if not configuracoes["planilha"] in sheet_names.sheet_names:
        log = lod_processamento.objects.create(
            projeto=ged.projeto,
            tipo="GED_PROCESSAMENTO",
            log="Planilha " + configuracoes["planilha"] + " não foi encontrada",
            execucao=ged,

        )
        ged.status = 'ERRO'
        ged.save()

    if ged.status != "ERRO":
    ################################leitura do excel

        df_ged = pd.read_excel(arquivold_file, sheet_name =configuracoes["planilha"], skiprows = int(configuracoes["linha"]))

    ################################remove colunas em branco

        if int(configuracoes["coluna"]) != 0:
            df_ged = df_ged.drop(columns=df_ged.columns[0:int(configuracoes["coluna"])])

    ################################remove colunas em branco
        df_ged = df_ged.rename(columns=df_ged.iloc[0])

    ################################renomeia o nome das colunas
        df_ged = df_ged.rename(columns=df_ged.iloc[0])
        df_ged = df_ged.drop(df_ged.index[0])

    ################################validando colunas
        valida_colunadf(df_ged,ged,configuracoes)
        if ged.status != "ERRO":



            for dado in range(len(df_ged)):
                try:
                    documento = df_ged[configuracoes["documento"]].iloc[dado]
                except:
                    pass
                revisao = df_ged[configuracoes["revisao"]].iloc[dado]
                tipo_documento = df_ged[configuracoes["tipo_documento"]].iloc[dado]
                disciplina = df_ged[configuracoes["disciplina"]].iloc[dado]
                titulo_1 = df_ged[configuracoes["titulo_1"]].iloc[dado]
                titulo_2 = df_ged[configuracoes["titulo_2"]].iloc[dado]
                empresa = df_ged[configuracoes["empresa"]].iloc[dado]
                numero_contratada = df_ged[configuracoes["numero_contratada"]].iloc[dado]
                status_ged = df_ged[configuracoes["status_ged"]].iloc[dado]
                data_atualizacao = df_ged[configuracoes["data_atualizacao"]].iloc[dado]
                if type(data_atualizacao) == float:
                    data_atualizacao = None
                grd_recebimento = df_ged[configuracoes["grd_recebimento"]].iloc[dado]

                data_grd_recebimento = df_ged[configuracoes["data_grd_recebimento"]].iloc[dado]
                if type(data_grd_recebimento) == float:
                    data_grd_recebimento = None

                data_analise = df_ged[configuracoes["data_analise"]].iloc[dado]
                if type(data_analise) == float:
                    data_analise = None

                resultado_analise = df_ged[configuracoes["resultado_analise"]].iloc[dado]
                formato = df_ged[configuracoes["formato"]].iloc[dado]
                tipo_emissao = df_ged[configuracoes["tipo_emissao"]].iloc[dado]
                atual_responsavel = df_ged[configuracoes["atual_responsavel"]].iloc[dado]

                try:
                    certificado = FluxoEmissao.objects.get(owner=projeto.unidade.owner, sigla_devolucao=resultado_analise)
                    if certificado.certificado == 1:
                        certificado = "SIM"
                    else:
                        certificado = "NÃO"
                except:
                    certificado = " "

                try:
                    cancelado = FluxoEmissao.objects.get(owner=projeto.unidade.owner, sigla_devolucao=resultado_analise)
                    if cancelado.cancelado == 1:
                        cancelado = "SIM"
                    else:
                        cancelado = "NÃO"
                except:
                    cancelado = " "

                try:
                    documento_revisado = str(documento)+"_REV_"+str(revisao)
                except:
                    documento_revisado = ""

                try:
                    titulo = titulo_1 + titulo_2
                except:
                    titulo = ""

                carga_stage_ld = StageGED.objects.create(
                execucao = ged,
                projeto = ged.projeto,
                documento_revisao=documento_revisado,
                documento=documento,
                revisao=revisao,
                certificado=certificado,
                tipo_emissao=tipo_emissao,
                cancelado=cancelado,
                tipo_documento = tipo_documento,
                disciplina= disciplina,
                titulo=titulo, # conversar
                empresa=empresa,
                numero_contratada=numero_contratada,
                status_ged=status_ged,
                data_atualizacao=tratar_data(data_atualizacao),
                data_grd_recebimento=tratar_data(data_grd_recebimento),
                data_analise=tratar_data(data_analise),
                resultado_analise=resultado_analise,
                formato=formato,
                responsavel=atual_responsavel,
                rev_num="Conta"
                )


def valida_colunadf(df_ged,ged, configuracoes):
    print("Colunas DF########")
    print(df_ged.columns)
    print("DF DF########")

    colunas_errors = []
    if not configuracoes["documento"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["documento"] + " não foi encontrada")

    if not configuracoes["revisao"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["revisao"] + " não foi encontrada")

    if not configuracoes["tipo_documento"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["tipo_documento"] + " não foi encontrada")

    if not configuracoes["disciplina"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["disciplina"] + " não foi encontrada")

    if not configuracoes["titulo_1"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["titulo_1"] + " não foi encontrada")

    if not configuracoes["titulo_2"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["titulo_2"] + " não foi encontrada")

    if not configuracoes["empresa"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["empresa"] + " não foi encontrada")

    if not configuracoes["numero_contratada"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["numero_contratada"] + " não foi encontrada")

    if not configuracoes["status_ged"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["status_ged"] + " não foi encontrada")

    if not configuracoes["data_atualizacao"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["data_atualizacao"] + " não foi encontrada")

    if not configuracoes["grd_recebimento"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["grd_recebimento"] + " não foi encontrada")

    if not configuracoes["data_grd_recebimento"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["data_grd_recebimento"] + " não foi encontrada")

    if not configuracoes["data_analise"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["data_analise"] + " não foi encontrada")

    if not configuracoes["resultado_analise"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["resultado_analise"] + " não foi encontrada")

    if not configuracoes["formato"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["formato"] + " não foi encontrada")

    #if not configuracoes["work_package_area"] in df_ged.columns:
    #    colunas_errors.append("A Coluna "  + configuracoes["work_package_area"] + " não foi encontrada")

    #if not configuracoes["work_package"] in df_ged.columns:
    #    colunas_errors.append("A Coluna "  + configuracoes["work_package"] + " não foi encontrada")

    if not configuracoes["tipo_emissao"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["tipo_emissao"] + " não foi encontrada")

    if not configuracoes["atual_responsavel"] in df_ged.columns:
        colunas_errors.append("A Coluna "  + configuracoes["atual_responsavel"] + " não foi encontrada")


    if len(colunas_errors) > 0:

        for erro in colunas_errors:
            log = lod_processamento.objects.create(
                projeto=ged.projeto,
                tipo="GED_PROCESSAMENTO",
                log = erro,
                execucao = ged,

            )
        ged.status = 'ERRO'
        ged.save()

    else:
        pass






def criar_planilha_log(output, id):
    pass

    wb = xls.Workbook(output)

    log = wb.add_worksheet("log")  # LOGS


    planilha_logs(log, wb, id)


    wb.close()


def planilha_logs(log, wb, id):
    execucao = ExecucaoLD.objects.get(id=id)
    dados = lod_processamento.objects.filter(execucao=execucao)

    log.add_table(xl_util.xl_range_abs(0, 0, dados.count(), 1),
                      {'name': 'wp_type7', 'style': None, 'columns': [{'header': 'Tipo'},
                                                                      {'header': 'Log'},
                                                                      ]})

    log.write_row(0, 0, ['Tipo', 'Log'],
                      wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '11'}))

    row_num = 1

    for dado in dados:
        if row_num % 2 == 0:
            log.write(row_num, 0, dado.tipo)
            log.write(row_num, 1, dado.log)

        else:
            log.write(row_num, 0, dado.tipo, wb.add_format({'bg_color': '#bfbfbf'}))
            log.write(row_num, 1, dado.log, wb.add_format({'bg_color': '#bfbfbf'}))


        row_num += 1

    log.hide_gridlines(2)
    log.set_column('A:A', 40.00)
    log.set_column('B:B', 60.00)

    log.set_row(0, 40.0)
    log.set_tab_color('green')