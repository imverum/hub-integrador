import pandas as pd
from apps.ged.models import lod_processamento, ExecucaoLD
from apps.master_index.models import ConfiguraMasterIndexCWA, LogProcessamentoMasterIndex, StageMasterIndexCWA, \
    ADFMasterIndexCWA

from apps.projeto.models import Projeto
import xlsxwriter as xls
import xlsxwriter.utility as xl_util

def run_cwa(arquivold_file, projeto_id, cwa, request):

    projeto = Projeto.objects.get(id=projeto_id)
    configuracoes = ConfiguraMasterIndexCWA.objects.filter(projeto=projeto).values().first()

    sheet_names = pd.ExcelFile(arquivold_file)
    if not configuracoes["planilha"] in sheet_names.sheet_names:
        log = LogProcessamentoMasterIndex.objects.create(
            projeto=cwa.projeto,
            tipo="CWA_PROCESSAMENTO",
            log="Planilha " + configuracoes["planilha"] + " não foi encontrada",
            execucao=cwa,

        )
        cwa.status = 'ERRO'
        cwa.save()

    if cwa.status != "ERRO":
    ################################leitura do excel

        df_cwa = pd.read_excel(arquivold_file, sheet_name =configuracoes["planilha"], skiprows = int(configuracoes["linha"]))

    ################################remove colunas em branco

        df_cwa = df_cwa.drop(columns=df_cwa.columns[0:int(configuracoes["coluna"])])


    ################################validando colunas
        valida_colunadf(df_cwa,cwa,request, configuracoes)
        if cwa.status != "ERRO":



            for dado in range(len(df_cwa)):

                codigo_do_projeto = df_cwa[configuracoes["codigo_do_projeto"]].iloc[dado]
                if pd.isna(codigo_do_projeto):
                    codigo_do_projeto = None

                codigo_cwa = df_cwa[configuracoes["codigo_cwa"]].iloc[dado]
                if pd.isna(codigo_cwa):
                    codigo_cwa = None


                descricao = df_cwa[configuracoes["descricao"]].iloc[dado]
                if pd.isna(descricao):
                    descricao = None

                coordenadas = df_cwa[configuracoes["coordenadas"]].iloc[dado]
                if pd.isna(coordenadas):
                    coordenadas = None

                nivel_do_solo = df_cwa[configuracoes["nivel_do_solo"]].iloc[dado]
                if pd.isna(nivel_do_solo):
                    nivel_do_solo = None


                carga_stage_cwa = StageMasterIndexCWA.objects.create(
                execucao = cwa,
                projeto=cwa.projeto,
                data_corte=cwa.data_corte,
                data_execucao=cwa.data_execucao,

                codigo_do_projeto = codigo_do_projeto,
                codigo_cwa = codigo_cwa,
                descricao = descricao,
                coordenadas = coordenadas,
                nivel_do_solo= nivel_do_solo,

                )

            carga_adf_cwa = ADFMasterIndexCWA.objects.create(
                execucao = cwa,
            )


def valida_colunadf(df_cwa,cwa, request, configuracoes ):
    colunas_errors = []
    if not configuracoes["codigo_do_projeto"] in df_cwa.columns:

        colunas_errors.append("A Coluna "  + configuracoes["codigo_do_projeto"] + " não foi encontrada")

    if not configuracoes["codigo_cwa"] in df_cwa.columns:

        colunas_errors.append("A Coluna "  + configuracoes["codigo_cwa"] + " não foi encontrada")

    if not configuracoes["descricao"] in df_cwa.columns:

        colunas_errors.append("A Coluna "  + configuracoes["descricao"] + " não foi encontrada")

    if not configuracoes["coordenadas"] in df_cwa.columns:

        colunas_errors.append("A Coluna "  + configuracoes["coordenadas"] + " não foi encontrada")

    if not configuracoes["nivel_do_solo"] in df_cwa.columns:

        colunas_errors.append("A Coluna "  + configuracoes["nivel_do_solo"] + " não foi encontrada")



    if len(colunas_errors) > 0:
        for erro in colunas_errors:
            log = LogProcessamentoMasterIndex.objects.create(
                projeto=cwa.projeto,
                tipo="CWA_PROCESSAMENTO",
                log = erro,
                execucao = cwa,

            )
        cwa.status = 'ERRO'
        cwa.save()

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