import pandas as pd
from apps.ged.models import StageLd, FluxoEmissao, ConfiguraLd, lod_processamento, ExecucaoLD, ADFLD

from apps.projeto.models import Projeto
import xlsxwriter as xls
import xlsxwriter.utility as xl_util

def run_ld(arquivold_file, projeto_id, ld, request):

    projeto = Projeto.objects.get(id=projeto_id)
    configuracoes = ConfiguraLd.objects.filter(projeto=projeto).values().first()

    sheet_names = pd.ExcelFile(arquivold_file)
    if not configuracoes["planilha"] in sheet_names.sheet_names:
        log_ld = lod_processamento.objects.create(
            projeto=ld.projeto,
            tipo="LD_PROCESSAMENTO",
            log="Planilha " + configuracoes["planilha"] + " não foi encontrada",
            execucao=ld,

        )
        ld.status = 'ERRO'
        ld.save()

    if ld.status != "ERRO":
    ################################leitura do excel

        df_ld = pd.read_excel(arquivold_file, sheet_name =configuracoes["planilha"], skiprows = int(configuracoes["linha"]))

    ################################remove colunas em branco

        df_ld = df_ld.drop(columns=df_ld.columns[0:int(configuracoes["coluna"])])

    ################################remove colunas em branco
        df_ld = df_ld.rename(columns=df_ld.iloc[0])

    ################################renomeia o nome das colunas
        df_ld = df_ld.rename(columns=df_ld.iloc[0])
        df_ld = df_ld.drop(df_ld.index[0])

    ################################validando colunas
        valida_colunadf(df_ld,ld,request, configuracoes)
        if ld.status != "ERRO":



            for dado in range(len(df_ld)):
                try:
                    documento = df_ld[configuracoes["documento"]].iloc[dado]
                    print("passou")
                except:
                    print("erro aqui")
                numero_contratada = df_ld[configuracoes["numero_contratada"]].iloc[dado]
                #titulo = df_ld[str(configuracoes.titulo)].iloc[dado]
                status_ld = df_ld[configuracoes["status_ld"]].iloc[dado]
                codigo_atividade = df_ld[configuracoes["codigo_atividade"]].iloc[dado]

                data_emissao_preliminar = df_ld[configuracoes["data_emissão_inicial_prevista"]].iloc[dado]

                if type(data_emissao_preliminar) == float:
                    data_emissao_preliminar = None


                pagina = df_ld[configuracoes["paginas"]].iloc[dado]
                a1_equivalente = df_ld[configuracoes["a1_equivalente"]].iloc[dado]
                tipo_emissao = df_ld[configuracoes["tipo_emissao"]].iloc[dado]

                try:
                    certifica = FluxoEmissao.objects.get(owner=projeto.unidade.owner, sigla_tipo_emissao=tipo_emissao)
                    if certifica.certifica_primeira_emissão == 1:
                        certifica = "SIM"
                    else:
                        certifica = "NÃO"
                except:
                    certifica = " "
                    print(certifica)


                carga_stage_ld = StageLd.objects.create(
                execucao = ld,
                projeto=ld.projeto,
                documento = documento,
                numero_contratada = numero_contratada,
                empresa = ld.fornecedor,
                tipo_emissao_inicial = tipo_emissao,
                certifica_na_1a_emissao= certifica,
                data_emissão_inicial_prevista=data_emissao_preliminar,
                status_ld=status_ld,
                paginas=pagina,
                a1_equivalente=a1_equivalente,
                codigo_atividade=codigo_atividade,
                )

            carga_adf_ld = ADFLD.objects.create(
                execucao=ld,
            )


def valida_colunadf(df_ld,ld, request, configuracoes ):
    colunas_errors = []
    if not configuracoes["documento"] in df_ld.columns:
        print("deu true")
        colunas_errors.append("A Coluna "  + configuracoes["documento"] + " não foi encontrada")

    if not configuracoes["numero_contratada"] in df_ld.columns:
        print("deu true")
        colunas_errors.append("A Coluna "  + configuracoes["numero_contratada"] + " não foi encontrada")

    if not configuracoes["status_ld"] in df_ld.columns:
        print("deu true")
        colunas_errors.append("A Coluna "  + configuracoes["status_ld"] + " não foi encontrada")

    if not configuracoes["codigo_atividade"] in df_ld.columns:
        print("deu true")
        colunas_errors.append("A Coluna "  + configuracoes["codigo_atividade"] + " não foi encontrada")

    if not configuracoes["data_emissão_inicial_prevista"] in df_ld.columns:
        print("deu true")
        colunas_errors.append("A Coluna "  + configuracoes["data_emissão_inicial_prevista"] + " não foi encontrada")

    if not configuracoes["paginas"] in df_ld.columns:
        print("deu true")
        colunas_errors.append("A Coluna "  + configuracoes["paginas"] + " não foi encontrada")

    if not configuracoes["a1_equivalente"] in df_ld.columns:
        print("deu true")
        colunas_errors.append("A Coluna "  + configuracoes["a1_equivalente"] + " não foi encontrada")

    if not configuracoes["tipo_emissao"] in df_ld.columns:
        print("deu true")
        colunas_errors.append("A Coluna "  + configuracoes["tipo_emissao"] + " não foi encontrada")


    if len(colunas_errors) > 0:
        print("entrou aqui")
        log_ld = lod_processamento.objects.create(
            projeto=ld.projeto,
            tipo="LD_PROCESSAMENTO",
            log = colunas_errors,
            execucao = ld,

        )
        ld.status = 'ERRO'
        ld.save()

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