import pandas as pd

from apps.core.tratar_datas import tratar_data
from apps.cronograma_master.models import StageCronogramaMasterBaseline, ADFCronoMasterCronogramas, \
    LogProcessamentoCronogramaMaster
from apps.ged.models import StageLd, FluxoEmissao, ConfiguraLd, lod_processamento, ExecucaoLD, ConfiguraGED, StageGED, \
    ADFGED
from datetime import datetime
from apps.projeto.models import Projeto
import xlsxwriter as xls
import xlsxwriter.utility as xl_util

def run_crono_master_baseline(arquivo_file, projeto, crono, request, container):
    projeto = Projeto.objects.get(id=projeto)
    configuracoes = ConfiguraGED.objects.filter(projeto=projeto).values().first()
    print(configuracoes)

    sheet_names = pd.ExcelFile(arquivo_file)
    if not "Baseline" in sheet_names.sheet_names:
        log = LogProcessamentoCronogramaMaster.objects.create(
            projeto=crono.projeto,
            tipo="BASELINE_PROCESSAMENTO",
            log="Planilha " + "Baseline" + " não foi encontrada",
            execucao=crono,

        )
        crono.status = 'ERRO'
        crono.save()

    if crono.status != "ERRO":
        ################################leitura do excel

        df_bl = pd.read_excel(arquivo_file, sheet_name="Baseline",
                               skiprows=0)

        ################################remove colunas em branco

        if 0 != 0:
            df_bl = df_bl.drop(columns=df_bl.columns[0:0])

        ################################validando colunas
        valida_colunadf(df_bl, crono, configuracoes)
        if crono.status != "ERRO":

            for dado in range(len(df_bl)):

                codigo = df_bl["Código"].iloc[dado]
                descricao_atividade = df_bl["Descrição Atividade"].iloc[dado]
                inicio = df_bl["Início"].iloc[dado]
                termino = df_bl["Término"].iloc[dado]
                duracao = df_bl["Duração"].iloc[dado]

                carga_stage_baseline = StageCronogramaMasterBaseline.objects.create(
                    execucao=crono,
                    projeto=crono.projeto,
                    container=container,

                    codigo=codigo,
                    descricao_atividade=descricao_atividade,
                    inicio=inicio,
                    termino=termino,
                    duracao=duracao,

                )
            carga_xer_adf_crono = ADFCronoMasterCronogramas.objects.create(
                execucao=crono,
                status_execucao_adf="Pendente",
                arquivo="Baseline",
                projeto=crono.projeto
            )


def valida_colunadf(df_bl, crono, configuracoes):
    print("Colunas DF########")
    print(df_bl.columns)
    print("DF DF########")

    colunas_errors = []
    if not "Código" in df_bl.columns:
        colunas_errors.append("A Coluna " + "Código" + " não foi encontrada")

    if not "Descrição Atividade" in df_bl.columns:
        colunas_errors.append("A Coluna " + "Descrição Atividade" + " não foi encontrada")

    if not "Início" in df_bl.columns:
        colunas_errors.append("A Coluna " + "Início" + " não foi encontrada")

    if not "Término" in df_bl.columns:
        colunas_errors.append("A Coluna " + "Término" + " não foi encontrada")

    if not "Duração" in df_bl.columns:
        colunas_errors.append("A Coluna " + "Duração" + " não foi encontrada")



    if len(colunas_errors) > 0:

        for erro in colunas_errors:
            log = LogProcessamentoCronogramaMaster.objects.create(
                projeto=crono.projeto,
                tipo="BASELINE_PROCESSAMENTO",
                log=erro,
                execucao=crono,

            )
        crono.status = 'ERRO'
        crono.save()

    else:
        pass