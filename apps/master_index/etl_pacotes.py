import pandas as pd
from apps.ged.models import StageLd, FluxoEmissao, ConfiguraLd, lod_processamento, ExecucaoLD
from apps.master_index.models import ConfiguraMasterIndexPacotes, StageMasterIndexPacotes, ADFMasterIndexPACOTES
import numpy as np
from apps.projeto.models import Projeto
import xlsxwriter as xls
import xlsxwriter.utility as xl_util

def run_pacotes(arquivold_file, projeto_id, pacotes, request):

    projeto = Projeto.objects.get(id=projeto_id)
    configuracoes = ConfiguraMasterIndexPacotes.objects.filter(projeto=projeto).values().first()

    sheet_names = pd.ExcelFile(arquivold_file)
    if not configuracoes["planilha"] in sheet_names.sheet_names:
        log = lod_processamento.objects.create(
            projeto=pacotes.projeto,
            tipo="PACOTES_PROCESSAMENTO",
            log="Planilha " + configuracoes["planilha"] + " não foi encontrada",
            execucao=pacotes,

        )
        pacotes.status = 'ERRO'
        pacotes.save()

    if pacotes.status != "ERRO":
    ################################leitura do excel

        df_pacotes = pd.read_excel(arquivold_file, sheet_name =configuracoes["planilha"], skiprows = int(configuracoes["linha"]))

    ################################remove colunas em branco

        df_pacotes = df_pacotes.drop(columns=df_pacotes.columns[0:int(configuracoes["coluna"])])


    ################################validando colunas
        valida_colunadf(df_pacotes,pacotes,request, configuracoes)
        if pacotes.status != "ERRO":



            for dado in range(len(df_pacotes)):

                codigo_do_projeto = df_pacotes[configuracoes["codigo_do_projeto"]].iloc[dado]
                if pd.isna(codigo_do_projeto):
                    codigo_do_projeto = None

                codigo_do_pacote = df_pacotes[configuracoes["codigo_do_pacote"]].iloc[dado]
                if pd.isna(codigo_do_pacote):
                    codigo_do_pacote = None


                descricao = df_pacotes[configuracoes["descricao"]].iloc[dado]
                if pd.isna(descricao):
                    descricao = None

                contrato = df_pacotes[configuracoes["contrato"]].iloc[dado]
                if pd.isna(contrato):
                    contrato = None

                cwa = df_pacotes[configuracoes["cwa"]].iloc[dado]
                if pd.isna(cwa):
                    cwa = None


                cwp = df_pacotes[configuracoes["cwp"]].iloc[dado]
                if pd.isna(cwp):
                    cwp = None

                subarea = df_pacotes[configuracoes["subarea"]].iloc[dado]
                if pd.isna(subarea):
                    subarea = None

                disciplina = df_pacotes[configuracoes["disciplina"]].iloc[dado]
                if pd.isna(disciplina):
                    disciplina = None

                subdisciplina = df_pacotes[configuracoes["subdisciplina"]].iloc[dado]
                if pd.isna(subdisciplina):
                    subdisciplina = None

                tipo = df_pacotes[configuracoes["tipo"]].iloc[dado]
                if pd.isna(tipo):
                    tipo = None

                status = df_pacotes[configuracoes["status"]].iloc[dado]
                if pd.isna(status):
                    status = None

                custo = df_pacotes[configuracoes["custo"]].iloc[dado]
                if pd.isna(custo):
                    custo = None

                responsavel = df_pacotes[configuracoes["responsavel"]].iloc[dado]
                if pd.isna(responsavel):
                    responsavel = None

                horas_estimadas = df_pacotes[configuracoes["horas_estimadas"]].iloc[dado]
                if pd.isna(horas_estimadas):
                    horas_estimadas = None

                carga_stage_pacotes = StageMasterIndexPacotes.objects.create(
                execucao = pacotes,
                projeto=pacotes.projeto,
                data_corte=pacotes.data_corte,
                data_execucao=pacotes.data_execucao,

                codigo_do_projeto = codigo_do_projeto,
                codigo_do_pacote = codigo_do_pacote,
                descricao = descricao,
                contrato = contrato,
                cwa= cwa,
                cwp=cwp,
                subarea=subarea,
                disciplina=disciplina,
                subdisciplina=subdisciplina,
                tipo=tipo,
                status=status,
                custo=custo,
                responsavel=responsavel,
                horas_estimadas=horas_estimadas,
                )

            carga_adf_pacotes = ADFMasterIndexPACOTES.objects.create(
                execucao=pacotes,
            )


def valida_colunadf(df_pacotes,pacotes, request, configuracoes ):
    colunas_errors = []
    if not configuracoes["codigo_do_projeto"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["codigo_do_projeto"] + " não foi encontrada")

    if not configuracoes["codigo_do_pacote"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["codigo_do_pacote"] + " não foi encontrada")

    if not configuracoes["descricao"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["descricao"] + " não foi encontrada")

    if not configuracoes["contrato"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["contrato"] + " não foi encontrada")

    if not configuracoes["cwa"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["cwa"] + " não foi encontrada")

    if not configuracoes["cwp"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["cwp"] + " não foi encontrada")

    if not configuracoes["subarea"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["subarea"] + " não foi encontrada")

    if not configuracoes["disciplina"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["disciplina"] + " não foi encontrada")

    if not configuracoes["subdisciplina"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["subdisciplina"] + " não foi encontrada")

    if not configuracoes["tipo"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["tipo"] + " não foi encontrada")

    if not configuracoes["status"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["status"] + " não foi encontrada")

    if not configuracoes["custo"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["custo"] + " não foi encontrada")

    if not configuracoes["responsavel"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["responsavel"] + " não foi encontrada")

    if not configuracoes["horas_estimadas"] in df_pacotes.columns:

        colunas_errors.append("A Coluna "  + configuracoes["horas_estimadas"] + " não foi encontrada")


    if len(colunas_errors) > 0:
        for erro in colunas_errors:
            log = lod_processamento.objects.create(
                projeto=pacotes.projeto,
                tipo="PACOTES_PROCESSAMENTO",
                log = erro,
                execucao = pacotes,

            )
        pacotes.status = 'ERRO'
        pacotes.save()

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