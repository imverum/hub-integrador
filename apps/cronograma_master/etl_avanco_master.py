from apps.core.tratar_datas import tratar_data, validar_data
from apps.cronograma_master.models import ConfiguraCronogramaMaster, LogProcessamentoCronogramaMaster, \
    StageCronogramaMaster, ADFCronoMaster, ADFCronoMasterCronogramas, TabelaTaskAvancoMaster, TabelaTaskrsrcAvancoMaster
from apps.cronogramacontratadas.models import StageCronogramaContratadaAtividade
from apps.projeto.models import Projeto
import pandas as pd
import numpy as np
from datetime import datetime

def formatar_data(data):
    if pd.notna(data):  # Verifique se o valor não é NaN ou NaT
        return data.strftime("%d/%m/%Y %H:%M:%S")
    else:
        return None

def converter_percentual(valor_percentual):
    try:
        valor_sem_percentual = valor_percentual.replace('%', '').replace(',', '.')
        valor_decimal = float(valor_sem_percentual) / 100.0  # Converta para decimal
        return valor_decimal
    except:

        return float(valor_percentual)


def run_avanco_master(arquivo_file, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)

    ################################leitura do excel

    df_crono = pd.read_excel(arquivo_file, sheet_name="TASK", skiprows=1)

    ################################remove colunas em branco


    df_crono["Activity ID"] = df_crono["Activity ID"].apply(
        lambda id: None if pd.isna(id) else id)

    df_crono["Activity Status"] = df_crono["Activity Status"].apply(
        lambda OP_WP: None if pd.isna(OP_WP) else OP_WP)

    df_crono['WBS Code'] = df_crono['WBS Code'].apply(
        lambda resource_name: None if pd.isna(resource_name) else resource_name)

    df_crono['OP_CWP'] = df_crono['OP_CWP'].apply(
        lambda resource_type: None if pd.isna(resource_type) else resource_type)

    df_crono['Activity Name'] = df_crono['Activity Name'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['OP_PACOTE DE SUPRIMENTOS'] = df_crono['OP_PACOTE DE SUPRIMENTOS'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Original Duration(d)'] = df_crono['Original Duration(d)'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Activity % Complete(%)'] = df_crono['Activity % Complete(%)'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Activity % Complete(%)'] = df_crono['Activity % Complete(%)'].apply(
        lambda spreadsheet_field: float(str(spreadsheet_field).replace(',', '.')) if ',' in str(
            spreadsheet_field) else spreadsheet_field
    )

    df_crono['(*)Start'] = df_crono['(*)Start'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['(*)Finish'] = df_crono['(*)Finish'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Actual Start'] = df_crono['Actual Start'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Actual Finish'] = df_crono['Actual Finish'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)


    df_crono = df_crono.rename(columns={'Activity ID': 'activity_id'})
    df_crono = df_crono.rename(columns={'Activity Status': 'activity_status'})
    df_crono = df_crono.rename(columns={'WBS Code': 'wbs_code'})
    df_crono = df_crono.rename(columns={'OP_CWP': 'op_cwp'})
    df_crono = df_crono.rename(columns={'OP_PACOTE DE SUPRIMENTOS': 'OP_PACOTE_DE_SUPRIMENTOS'})
    df_crono = df_crono.rename(columns={'Activity Name': 'activity_name'})
    df_crono = df_crono.rename(columns={'Original Duration(d)': 'target_drtn_hr_cnt'})
    df_crono = df_crono.rename(columns={'Activity % Complete(%)': 'complete_pct'})
    df_crono = df_crono.rename(columns={'(*)Start': 'start_date'})
    df_crono = df_crono.rename(columns={'(*)Finish': 'end_date'})
    df_crono = df_crono.rename(columns={'Actual Start': 'act_start_date'})
    df_crono = df_crono.rename(columns={'Actual Finish': 'act_end_date'})

    df_crono.drop('Delete This Row', axis=1,inplace=True)
    df_crono["projeto_id"]=projeto.id





    df_crono.to_excel('arquivo_tratado.xlsx', index=False)

    # Converter o DataFrame em uma lista de instâncias do modelo
    instancias = [TabelaTaskAvancoMaster(**dados) for dados in df_crono.to_dict('records')]

    # Inserir as instâncias no banco de dados
    TabelaTaskAvancoMaster.objects.bulk_create(instancias)


def run_avanco_master_recurso(arquivo_file, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)

    ################################leitura do excel

    df_crono = pd.read_excel(arquivo_file, sheet_name="TASKRSRC", skiprows=1)


    ################################remove colunas em branco


    df_crono["Resource ID"] = df_crono["Resource ID"].apply(
        lambda id: None if pd.isna(id) else id)

    df_crono["Activity ID"] = df_crono["Activity ID"].apply(
        lambda OP_WP: None if pd.isna(OP_WP) else OP_WP)

    df_crono['(*)Activity Status'] = df_crono['(*)Activity Status'].apply(
        lambda resource_name: None if pd.isna(resource_name) else resource_name)

    df_crono['Role ID'] = df_crono['Role ID'].apply(
        lambda resource_type: None if pd.isna(resource_type) else resource_type)

    df_crono['Cost Account ID'] = df_crono['Cost Account ID'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['(*)Resource Type'] = df_crono['(*)Resource Type'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Actual Start'] = df_crono['Actual Start'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Actual Finish'] = df_crono['Actual Finish'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Budgeted Units(h)'] = df_crono['Budgeted Units(h)'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Budgeted Units(h)'] = df_crono['Budgeted Units(h)'].apply(
        lambda spreadsheet_field: float(str(spreadsheet_field).replace(',', '.')) if ',' in str(
            spreadsheet_field) else spreadsheet_field
    )

    df_crono['Actual Units(h)'] = df_crono['Actual Units(h)'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Actual Units(h)'] = df_crono['Actual Units(h)'].apply(
        lambda spreadsheet_field: float(str(spreadsheet_field).replace(',', '.')) if ',' in str(
            spreadsheet_field) else spreadsheet_field
    )

    df_crono['Remaining Early Units(h)'] = df_crono['Remaining Early Units(h)'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Remaining Early Units(h)'] = df_crono['Remaining Early Units(h)'].apply(
        lambda spreadsheet_field: float(str(spreadsheet_field).replace(',', '.')) if ',' in str(
            spreadsheet_field) else spreadsheet_field
    )

    df_crono['Budgeted Cost'] = df_crono['Budgeted Cost'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Budgeted Cost'] = df_crono['Budgeted Cost'].apply(
        lambda spreadsheet_field: float(str(spreadsheet_field).replace(',', '.')) if ',' in str(
            spreadsheet_field) else spreadsheet_field
    )

    df_crono['Actual Cost'] = df_crono['Actual Cost'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Actual Cost'] = df_crono['Actual Cost'].apply(
        lambda spreadsheet_field: float(str(spreadsheet_field).replace(',', '.')) if ',' in str(
            spreadsheet_field) else spreadsheet_field
    )

    df_crono['Remaining Cost'] = df_crono['Remaining Cost'].apply(
        lambda spreadsheet_field: None if pd.isna(spreadsheet_field) else spreadsheet_field)

    df_crono['Remaining Cost'] = df_crono['Remaining Cost'].apply(
        lambda spreadsheet_field: float(str(spreadsheet_field).replace(',', '.')) if ',' in str(
            spreadsheet_field) else spreadsheet_field
    )


    df_crono = df_crono.rename(columns={'Resource ID': 'rsrc_id'})
    df_crono = df_crono.rename(columns={'Activity ID': 'activity_id'})
    df_crono = df_crono.rename(columns={'(*)Activity Status': 'task_status_code'})
    df_crono = df_crono.rename(columns={'Role ID': 'role_id'})
    df_crono = df_crono.rename(columns={'Cost Account ID': 'acct_id'})
    df_crono = df_crono.rename(columns={'(*)Resource Type': 'rsrc_type'})
    df_crono = df_crono.rename(columns={'Actual Start': 'act_start_date'})
    df_crono = df_crono.rename(columns={'Actual Finish': 'act_end_date'})
    df_crono = df_crono.rename(columns={'Budgeted Units(h)': 'target_qty'})
    df_crono = df_crono.rename(columns={'Actual Units(h)': 'act_qty'})
    df_crono = df_crono.rename(columns={'Remaining Early Units(h)': 'remain_qty'})
    df_crono = df_crono.rename(columns={'Budgeted Cost': 'target_cost'})
    df_crono = df_crono.rename(columns={'Actual Cost': 'act_cost'})
    df_crono = df_crono.rename(columns={'Remaining Cost': 'remain_cost'})

    df_crono.drop('Delete This Row', axis=1, inplace=True)
    df_crono["projeto_id"]=projeto.id



    # Converter o DataFrame em uma lista de instâncias do modelo
    instancias = [TabelaTaskrsrcAvancoMaster(**dados) for dados in df_crono.to_dict('records')]

    # Inserir as instâncias no banco de dados
    TabelaTaskrsrcAvancoMaster.objects.bulk_create(instancias)


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


