from apps.core.tratar_datas import tratar_data, validar_data
from apps.cronograma_master.models import ConfiguraCronogramaMaster, LogProcessamentoCronogramaMaster, \
    StageCronogramaMaster, ADFCronoMaster, ADFCronoMasterCronogramas
#from apps.cronogramacontratadas.carga_mpp import conector_project
from apps.cronogramacontratadas.carga_xer import _xer_loader, XerTableRender, cria_df_carga_xer
from apps.cronogramacontratadas.models import StageCronogramaContratadaAtividade
from apps.projeto.models import Projeto
import pandas as pd
import numpy as np
from decimal import Decimal
from datetime import datetime
import os
import tempfile
import shutil

def formatar_data(data):
    try:
        if pd.notna(data):  # Verifique se o valor não é NaN ou NaT
            return data.strftime("%d/%m/%Y %H:%M:%S")
        else:
            return None
    except:
        return None

def converter_percentual(valor_percentual):
    try:
        valor_sem_percentual = valor_percentual.replace('%', '').replace(',', '.')
        valor_decimal = float(valor_sem_percentual) / 100.0  # Converta para decimal
        return valor_decimal
    except:

        return float(valor_percentual)


def run_crono_contratada_atividades(arquivo_file, projeto_id, crono, data_corte, contratada_id, op_wp):
    projeto = Projeto.objects.get(id=projeto_id)

    if arquivo_file.name.endswith('xlsx'):
        ################################leitura do excel
        df_crono = pd.read_excel(arquivo_file, sheet_name="Atividades", skiprows=0)

    elif arquivo_file.name.endswith('xer'):
        with tempfile.NamedTemporaryFile(suffix='.xer', delete=False) as tmp_file:
            shutil.copyfileobj(arquivo_file, tmp_file)

            tmp_file.flush()
            tmp_file.seek(0)

            caminho_arquivo_temporario = os.path.join(tempfile.gettempdir(), tmp_file.name)
            print(caminho_arquivo_temporario)
        xer = _xer_loader(caminho_arquivo_temporario)
        xer_parser = XerTableRender(xer.tables)



        df_crono = cria_df_carga_xer(xer_parser, op_wp)
        df_crono["Work Package"] = "Work Package"

        df_crono.to_excel('carga.xlsx',index=False)

    # elif arquivo_file.name.endswith('mpp'):
    #     with tempfile.NamedTemporaryFile(suffix='.mpp', delete=False) as tmp_file:
    #         shutil.copyfileobj(arquivo_file, tmp_file)
    #
    #         tmp_file.flush()
    #         tmp_file.seek(0)
    #
    #         croonograma = os.path.join(tempfile.gettempdir(), tmp_file.name)
    #
    #         coluna ='Texto 3'
    #         df_crono = conector_project(croonograma, coluna)
    #         df_crono.to_excel('carga_mpp.xlsx', index=False)

    ################################remove colunas em branco

    colunas_datas_tratadas = []
    for coluna in df_crono.columns:
            try:
                data_str = coluna.strftime("%d/%m/%Y %H:%M:%S")
                colunas_datas_tratadas.append(data_str)
            except:
                colunas_datas_tratadas.append(coluna)

    df_crono.columns = colunas_datas_tratadas

    df_crono["ID"] = df_crono["ID"].apply(
        lambda id: None if pd.isna(id) else id)

    df_crono["OP_WP"] = df_crono["OP_WP"].apply(
        lambda OP_WP: None if pd.isna(OP_WP) else OP_WP)

    df_crono['Folga Livre'] = df_crono['Folga Livre'].apply(
        lambda resource_name: None if pd.isna(resource_name) else resource_name)

    df_crono['Folga Total'] = df_crono['Folga Total'].apply(
        lambda resource_type: None if pd.isna(resource_type) else resource_type)

    df_crono['Duração'] = df_crono['Duração'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)


    df_crono['Avanço'] = df_crono['Avanço'].apply(converter_percentual)
    df_crono["Avanço"] = df_crono["Avanço"].apply(
        lambda Valor: None if pd.isna(Valor) else Valor)

    df_crono['previsto'] = pd.to_numeric(df_crono['previsto'])
    df_crono['previsto'] = df_crono['previsto'].apply(lambda x: float(x) if pd.notna(x) else None)

    # df_crono["previsto"] = df_crono["previsto"].apply(
    #     lambda Valor: None if pd.isna(Valor) else Valor)

    df_crono['actual'] = pd.to_numeric(df_crono['actual'])
    df_crono['actual'] = df_crono['actual'].apply(lambda x: float(x) if pd.notna(x) else None)

    # df_crono["actual"] = df_crono["actual"].apply(
    #     lambda Valor: None if pd.isna(Valor) else Valor)

    df_crono['Data Início BL'] = df_crono['Data Início BL'].apply(formatar_data)
    df_crono['Data Início BL'] = df_crono['Data Início BL'].str.replace('-', '/')
    df_crono['Data Início BL'] = df_crono['Data Início BL'].apply(tratar_data)

    df_crono["Data Início BL"] = df_crono["Data Início BL"].apply(
        lambda Unidade: None if pd.isna(Unidade) else Unidade)

    df_crono['Data Fim BL'] = df_crono['Data Fim BL'].apply(formatar_data)
    df_crono['Data Fim BL'] = df_crono['Data Fim BL'].str.replace('-', '/')
    df_crono['Data Fim BL'] = df_crono['Data Fim BL'].apply(tratar_data)

    df_crono["Data Fim BL"] = df_crono["Data Fim BL"].apply(
        lambda valor: None if pd.isna(valor) else valor)

    df_crono['Data Início Reprogramado'] = df_crono['Data Início Reprogramado'].apply(formatar_data)
    df_crono['Data Início Reprogramado'] = df_crono['Data Início Reprogramado'].str.replace('-', '/')
    df_crono['Data Início Reprogramado'] = df_crono['Data Início Reprogramado'].apply(tratar_data)

    df_crono["Data Início Reprogramado"] = df_crono["Data Início Reprogramado"].apply(
        lambda Unidade: None if pd.isna(Unidade) else Unidade)

    df_crono['Data Fim Reprogramado'] = df_crono['Data Fim Reprogramado'].apply(formatar_data)
    df_crono['Data Fim Reprogramado'] = df_crono['Data Fim Reprogramado'].str.replace('-', '/')
    df_crono['Data Fim Reprogramado'] = df_crono['Data Fim Reprogramado'].apply(tratar_data)

    df_crono["Data Fim Reprogramado"] = df_crono["Data Fim Reprogramado"].apply(
        lambda Unidade: None if pd.isna(Unidade) else Unidade)

    df_crono['Data Início Real'] = df_crono['Data Início Real'].apply(formatar_data)
    df_crono['Data Início Real'] = df_crono['Data Início Real'].str.replace('-', '/')
    df_crono['Data Início Real'] = df_crono['Data Início Real'].apply(tratar_data)

    df_crono["Data Início Real"] = df_crono["Data Início Real"].apply(
        lambda valor: None if pd.isna(valor) else valor)

    df_crono['Data Fim Real'] = df_crono['Data Fim Real'].apply(formatar_data)
    df_crono['Data Fim Real'] = df_crono['Data Fim Real'].str.replace('-', '/')
    df_crono['Data Fim Real'] = df_crono['Data Fim Real'].apply(tratar_data)

    df_crono["Data Fim Real"] = df_crono["Data Fim Real"].apply(
        lambda Unidade: None if pd.isna(Unidade) else Unidade)


    df_crono["Work Package"] = df_crono["Work Package"].apply(
        lambda Unidade: None if pd.isna(Unidade) else Unidade)

    df_crono[['Folga Livre', 'Folga Total', 'Duração', 'Avanço']] = df_crono[['Folga Livre', 'Folga Total', 'Duração', 'Avanço']].fillna(0)

    df_crono.to_excel('arquivo.xlsx', index=False)

    df_crono = df_crono.rename(columns={'ID': 'activity_id'})
    df_crono = df_crono.rename(columns={'Folga Livre': 'folga_livre'})
    df_crono = df_crono.rename(columns={'Folga Total': 'folga_total'})
    df_crono = df_crono.rename(columns={'Duração': 'duracao'})
    df_crono = df_crono.rename(columns={'Avanço': 'avanco'})
    df_crono = df_crono.rename(columns={'Data Início BL': 'data_inicio_bl'})
    df_crono = df_crono.rename(columns={'Data Fim BL': 'data_fim_bl'})
    df_crono = df_crono.rename(columns={'Data Início Reprogramado': 'data_inicio_reprogramado'})
    df_crono = df_crono.rename(columns={'Data Fim Reprogramado': 'data_fim_reprogramado'})
    df_crono = df_crono.rename(columns={'Data Início Real': 'data_inicio_real'})
    df_crono = df_crono.rename(columns={'Data Fim Real': 'data_fim_real'})
    df_crono = df_crono.rename(columns={'Work Package': 'work_package'})
    df_crono = df_crono.rename(columns={'OP_WP': 'OP_WP'})

    df_crono["execucao_id"]=crono.id
    df_crono["projeto_id"]=crono.projeto.id
    df_crono["contratada_id"]=contratada_id
    df_crono["data_corte"]=data_corte
    df_crono = df_crono.replace(np.nan, None)

    df_crono.to_excel('arquivo_tratado.xlsx', index=False)

    # Converter o DataFrame em uma lista de instâncias do modelo
    instancias = [StageCronogramaContratadaAtividade(**dados) for dados in df_crono.to_dict('records')]

    # Inserir as instâncias no banco de dados




    StageCronogramaContratadaAtividade.objects.bulk_create(instancias)


def valida_colunadf(df_crono, crono, request, configuracoes):
    colunas_errors = []
    if not configuracoes["activity_id"] in df_crono.columns:

        colunas_errors.append("A Coluna " + configuracoes["activity_id"] + " não foi encontrada")

    if not configuracoes["resource_name"] in df_crono.columns:

        colunas_errors.append("A Coluna " + configuracoes["resource_name"] + " não foi encontrada")

    if not configuracoes["resource_type"] in df_crono.columns:

        colunas_errors.append("A Coluna " + configuracoes["resource_type"] + " não foi encontrada")

    if not configuracoes["spreadsheet_field"] in df_crono.columns:

        colunas_errors.append("A Coluna " + configuracoes["spreadsheet_field"] + " não foi encontrada")


    if len(colunas_errors) > 0:
        for erro in colunas_errors:

            log = LogProcessamentoCronogramaMaster.objects.create(
                projeto=crono.projeto,
                tipo="CRONO_MASTER_PROCESSAMENTO",
                log=erro,
                execucao=crono,

            )
        crono.status = 'ERRO'
        crono.save()

    else:
        pass


