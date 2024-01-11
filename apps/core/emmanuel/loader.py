from sqlalchemy import create_engine
import requests
from io import BytesIO
from xerparser import Xer
import re
import pandas as pd
import pyodbc
import math
import os
import datetime as dt
from apps.cronogramacontratadas.carga_xer import XerTableRender, CurvaRecursos, Calendars




db_tables = [
    'XER.ACTVCODE',
    'XER.ACTVTYPE',
    'XER.CALENDAR',
    'XER.PROJECT',
    'XER.PROJWBS',
    'XER.RSRC',
    'XER.TASK',
    'XER.TASKACTV',
    'XER.TASKPRED',
    'XER.UDFTYPE',
    'XER.UDFVALUE'
]

# conn_str = (
#     "Driver={ODBC Driver 17 for SQL Server};"
#     "Server=onca-puma.database.windows.net;"
#     "Database=DB_Verum_IPE;"
#     "uid=emmanuelsantana;"
#     "pwd=Recife@2023"
# )
# cnxn = pyodbc.connect(conn_str)
# engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn_str))




def get_baseline_table(xer_path):
    start_date = (2022, 2, 1)
    end_date = (2025, 12, 30)

    xer = _xer_loader(xer_path)
    xer_parser = XerTableRender(xer.tables)

    df_tasks = xer_parser.render_table('TASK')
    df_baseline = df_tasks[[
        'task_code',
        'task_name',
        'start_date',
        'target_start_date',
        'target_end_date',
        'end_date',
        'clndr_id',
    ]]

    def render_worked_days(row, calendar):
        df_worked_days = calendar.calculate_worked_days(row['start_date'], row['end_date'])
        df_worked_days['task_code'] = row['task_code']
        return df_worked_days

    calendars = Calendars(xer, start_date, end_date)
    calendars.pre_render_calendars()
    df_worked_days = pd.concat(df_baseline.apply(
        lambda row: render_worked_days(row, calendars.calculate_worked_days(row['clndr_id']))
        , axis=1
    ).tolist())

    df_worked_days = df_worked_days.groupby('task_code', as_index=False)['worked_days'].sum()
    df_worked_days['duracao_original'] = df_worked_days['worked_days'].apply(
        lambda x: math.floor(x) if (x % 1) < 0.5 else math.ceil(x))
    df_baseline = pd.merge(
        df_baseline,
        df_worked_days.drop_duplicates(subset=['task_code']),
        on='task_code',
        how='left'
    ).fillna(0)

    df_baseline = df_baseline.drop(columns=['clndr_id'])
    return df_baseline




def _curva(file_path, execucao_id, bl_path, engine,cnxn, projeto_id):
    # output_path = os.path.join(output_dir, str(execucao_id))
    # if not os.path.exists(output_path):
    #     os.makedirs(output_path)
    print('Loading Curve...')
    columns_mapper = {
        'activity_id': 'task_code',
        'rsrc_name': 'resource_name',
        'rsrc_type': 'resource_type',
        'date': 'data',
        'worked_units': 'valor',
    }
    curva_corrente = CurvaRecursos(file_path)
    df_curva_corrente = curva_corrente.get_table()
    df_curva_corrente = df_curva_corrente.loc[df_curva_corrente['spreadsheet_field'] != "Budgeted Units"]

    #[bl_curve] = [os.path.join(bl_path, item) for item in os.listdir(bl_path) if '.xlsx' in item]
    curva_bl = CurvaRecursos(bl_path)
    df_curva_bl = curva_bl.get_table()
    df_curva_bl = df_curva_bl.loc[df_curva_bl['spreadsheet_field'] == "Budgeted Units"]

    df_curva = pd.concat([df_curva_corrente, df_curva_bl], axis=0)
    df_curva = df_curva.rename(columns=columns_mapper)
    df_curva['ID_Arquivo'] = execucao_id
    df_curva['ID_Projeto'] = projeto_id
    df_curva['Chave_task_code'] = str(execucao_id) + "_" + df_curva['task_code']
    df_curva.to_sql(
        'Curva',
        schema='Cronograma_Master',
        con=engine,
        if_exists='append',
        index=False
    )
    # df_curva.to_parquet(
    #     os.path.join(output_path, 'df_curva.parquet'),
    # )



def _cronograma(file_path, execucao_id, bl_path_xer, engine, cnxn, projeto_id):
    # output_path = os.path.join(output_dir, str(execucao_id))
    # if not os.path.exists(output_path):
    #     os.makedirs(output_path)
    print('Loading .xer file...')
    
    xer = _xer_loader(file_path)
    xer_parser = XerTableRender(xer.tables)

    df_calendars = xer_parser.render_table('CALENDAR')
    df_projects = xer_parser.render_table('PROJECT')
    df_tasks = xer_parser.render_table('TASK')

    print('Starting pipeline: Arquivos')
    df_arquivos = df_projects[['last_recalc_date']].rename(columns={'last_recalc_date': 'Data_Atualizacao'})
    df_arquivos['ID_Arquivo'] = execucao_id
    df_arquivos['ID_Projeto'] = projeto_id

    print('Uploading table: Arquivos')

    df_arquivos[_get_table_columns('Arquivos', cnxn,'Cronograma_Master')].to_sql(
        'Arquivos',
        schema='Cronograma_Master',
        con=engine,
        if_exists='append',
        index=False
    )


    # df_arquivos[TableColumns.df_arquivos].to_parquet(
    #     os.path.join(output_path, 'df_arquivos.parquet'),
    #     index=False
    # )
    ##############################################################################################################
    print('Starting pipeline: Atividades')
    df_atividades = pd.merge(
        df_tasks,
        df_calendars[['clndr_id', 'day_hr_cnt']],
        how='left',
        on='clndr_id'
    )
    df_atividades.loc[df_atividades['status_code'] == 'TK_Active', 'status_code'] = 'In Progress'
    df_atividades.loc[df_atividades['status_code'] == 'TK_NotStart', 'status_code'] = 'Not Started'
    df_atividades.loc[df_atividades['status_code'] == 'TK_Complete', 'status_code'] = 'Complete'

    df_atividades['last_recalc_date'] = df_projects.loc[0, 'last_recalc_date']
    df_atividades['day_hr_cnt'] = df_atividades['day_hr_cnt'].fillna(8.)
    df_atividades['total_float_days'] = df_atividades['total_float_hr_cnt']/df_atividades['day_hr_cnt']
    df_atividades['free_float_days'] = df_atividades['free_float_hr_cnt']/df_atividades['day_hr_cnt']
    df_atividades['remain_drtn_days'] = df_atividades['remain_drtn_hr_cnt']/df_atividades['day_hr_cnt']
    df_atividades['target_drtn_days'] = df_atividades['target_drtn_hr_cnt']/df_atividades['day_hr_cnt']

    crit_path = [0, 5, 10, 15]
    for threshold in crit_path:
        df_atividades[f'Caminho_Critico_{threshold}_Dias'] = ''
        df_atividades.loc[df_atividades['total_float_days'] <=threshold, f'Caminho_Critico_{threshold}_Dias'] = 'Sim'
        df_atividades[f'Caminho_Critico_{threshold}_Dias'] = df_atividades[f'Caminho_Critico_{threshold}_Dias'].fillna('Não')

    df_atividades = df_atividades.drop(columns=['target_start_date', 'target_end_date'])

    print(bl_path_xer)

    df_atividades = pd.merge(
        df_atividades,
        get_baseline_table(bl_path_xer)[['task_code', 'target_start_date', 'target_end_date', 'duracao_original']],
        how='left',
        on='task_code'
    )

    df_atividades.loc[df_atividades['target_start_date'].isna(), 'target_start_date'] = df_atividades['start_date']
    df_atividades.loc[df_atividades['target_end_date'].isna(), 'target_end_date'] = df_atividades['end_date']
    df_atividades.loc[df_atividades['target_drtn_days'].isna(), 'target_end_date'] = df_atividades['target_end_date'] - df_atividades['target_start_date']
    df_atividades['status_atraso'] = ""
    df_atividades.loc[df_atividades['status_code'] == "Complete", 'status_atraso'] = "Início Atrasado"
    df_atividades.loc[
        (
            (df_atividades['target_end_date'] < df_atividades['last_recalc_date']) &
            (df_atividades['status_code'] == "Not Started")
        ),
        'status_atraso'
    ] = "Início Atrasado"
    df_atividades.loc[
        (
            (df_atividades['target_end_date'] < df_atividades['last_recalc_date']) & ### VERIFICAR CONTA
            (df_atividades['status_code'] == "Complete")
        ),
        'status_atraso'
    ] = "Término Atrasado"
    df_atividades.loc[
        (
            (df_atividades['target_end_date'] >= df_atividades['last_recalc_date']) &
            (df_atividades['status_code'] == "Not Started")
        ),
        'status_atraso'
    ] = "Não Iniciada com Risco de Atraso"
    df_atividades.loc[
        (
            (df_atividades['target_end_date'] >= df_atividades['last_recalc_date']) &
            (df_atividades['status_code'] == "In Progress")
        ),
        'status_atraso'
    ] = "Iniciada com Risco de Atraso"

    column_names = {
        'start_date': 'data_start',
        'end_date': 'data_end',
        'day_hr_cnt': 'horas_calendario',
    }
    df_atividades['ID_Projeto'] = projeto_id
    df_atividades['ID_Arquivo'] = execucao_id
    df_atividades['Chave_task_id'] = str(execucao_id) + '_' + df_atividades['task_id']
    df_atividades['Chave_task_code'] = str(execucao_id) + '_' + df_atividades['task_code']
    df_atividades = df_atividades.rename(columns=column_names)
    df_atividades['Start'] = df_atividades['Start'].astype(str)
    df_atividades['Finish'] = df_atividades['Finish'].astype(str)
    print('Uploading table: Atividades')
    df_atividades[_get_table_columns('Atividades', cnxn,'Cronograma_Master')].to_sql(
        'Atividades',
        schema='Cronograma_Master',
        con=engine,
        if_exists='append',
        index=False
    )
    # df_atividades[TableColumns.df_atividades].to_parquet(
    #     os.path.join(output_path, 'df_atividades.parquet'),
    #     index=False
    # )
    #####################################################################################################
    print('Starting pipeline: Predecessoras')
    column_names={
        'pred_task_id':'task_pred_id'
    }
    df_predecessora = xer_parser.render_table('TASKPRED')
    df_predecessora['pred_type'] = df_predecessora['pred_type'].replace('PR_', '')
    df_predecessora = pd.merge(
        df_predecessora,
        df_atividades,
        how='left',
        left_on='pred_task_id',
        right_on='task_id',
        suffixes=(None, '_predecessora')
    )
    column_names = {
        'start_date': 'data_start',
        'end_date': 'data_end',
        'day_hr_cnt': 'horas_calendario',
        'task_id_predecessora': 'pred.task_id',
        'status_code': 'pred.status_code',
        'task_code': 'pred.task_code',
        'task_name': 'pred.task_name',
        'data_start': 'pred.data_start',
        'data_end': 'pred.data_end',
        'driving_path_flag': 'pred.driving_path_flag',
        'Chave_task_code': 'Chave_task_code_predecessora'
    }
    df_predecessora['lag_days'] = df_predecessora['lag_hr_cnt'] / df_predecessora['horas_calendario']
    df_predecessora = df_predecessora.rename(columns=column_names)
    df_predecessora['Chave_task_id'] = str(execucao_id) + '_' + df_predecessora['task_id']
    df_predecessora['Chave_task_pred_id'] = str(execucao_id) + '_' + df_predecessora['task_pred_id']
    df_predecessora['ID_Projeto'] = projeto_id
    df_predecessora['ID_Arquivo'] = execucao_id
    print('Uploading table: Predecessoras')
    df_predecessora[_get_table_columns('Predecessoras', cnxn,'Cronograma_Master')].to_sql(
        'Predecessoras',
        schema='Cronograma_Master',
        con=engine,
        if_exists='append',
        index=False
    )
    # df_predecessora[TableColumns.df_predecessora].to_parquet(
    #     os.path.join(output_path, 'df_predecessora.parquet'),
    #     index=False
    # )
    # #####################################################################################################
    print('Starting pipeline: Consistencia_Qualidade')
    df_predecessora = df_predecessora[_get_table_columns('Predecessoras', cnxn,'Cronograma_Master')]
    df_predecessora['Link_FF'] = df_predecessora.loc[df_predecessora['pred_type'] == 'PR_FF'].groupby('Chave_task_id', as_index=False).transform('size')
    df_predecessora['Link_FS'] = df_predecessora.loc[df_predecessora['pred_type'] == 'PR_FS'].groupby('Chave_task_id', as_index=False).transform('size')
    df_predecessora['Link_SS'] = df_predecessora.loc[df_predecessora['pred_type'] == 'PR_SS'].groupby('Chave_task_id', as_index=False).transform('size')
    df_predecessora['Link_SF'] = df_predecessora.loc[df_predecessora['pred_type'] == 'PR_SF'].groupby('Chave_task_id', as_index=False).transform('size')
    df_predecessora['lag_days_menor_zero'] = df_predecessora.loc[df_predecessora['lag_days'] < 0].groupby('Chave_task_id', as_index=False).transform('size')

    df_predecessora['Chave_Predecessora'] = str(execucao_id) + '_' + df_predecessora['pred_task_id']
    df_predecessora['Quant_Sucessoras'] = df_predecessora.groupby('Chave_Predecessora', as_index=False).transform('size')
    
    column_names = [
        'Link_FF',
        'Link_FS',
        'Link_SS',
        'Link_SF',
        'lag_days_menor_zero',
        'Quant_Sucessoras',
    ]
    df_predecessora[column_names] = df_predecessora[column_names].fillna(0)
    
    
    df_atividades['termino_projeto'] = df_atividades['data_end'].max()
    df_qualidade = pd.merge(
        df_atividades,
        df_predecessora[['Chave_task_id','Link_FF','Link_FS','Link_SS','Link_SF','lag_days_menor_zero',]].drop_duplicates(subset='Chave_task_id', keep='first'),
        on='Chave_task_id',
        how='left',
        suffixes=(None, '_links')
    )
    df_qualidade = pd.merge(
        df_qualidade,
        df_predecessora[['Chave_Predecessora','Quant_Sucessoras',]].drop_duplicates(subset='Chave_Predecessora', keep='first'),
        left_on='Chave_task_id',
        right_on='Chave_Predecessora',
        how='left',
        suffixes=(None, '_predecessoras')
    )
    df_qualidade['Quant_Predecessoras'] = df_qualidade[['Link_FF', 'Link_FS', 'Link_SS', 'Link_SF']].sum(axis=1, numeric_only=True)
    df_qualidade['Total_Links'] = df_qualidade[['Quant_Predecessoras', 'Quant_Sucessoras']].sum(axis=1, numeric_only=True)
    df_qualidade['Atividades_Criticas'] = df_qualidade['Caminho_Critico_0_Dias'].apply(lambda x: "Crítica" if x == "Sim" else 'Não Crítica')
    df_qualidade['Sem_Predecessora'] = df_qualidade['Quant_Predecessoras'].apply(lambda x: "Sem Predecessoras" if x == 0 else 'ok')
    df_qualidade['Sem_Sucessora'] = df_qualidade['Quant_Sucessoras'].apply(lambda x: "Sem Predecessoras" if x == 0 else 'ok')
    df_qualidade['Finalizada_Sem_Avanco_100'] = df_qualidade.apply(lambda row: "Finalizada Sem Avanço 100%" if (row['status_code'] == "Complete") and (row['phys_complete_pct'] != 100) else 'ok', axis=1)
    df_qualidade['Iniciada_Sem_Avanco'] = df_qualidade.apply(lambda row: "Iniciada Sem Avanço" if (row['status_code'] != "Not Started") and (row['phys_complete_pct'] == 0) else 'ok', axis=1)
    df_qualidade['Nao_Iniciada_Com_Avanco'] = df_qualidade.apply(lambda row: "Não Iniciada Com Avanço" if (row['status_code'] == "Not Started") and (row['phys_complete_pct'] != 0) else 'ok', axis=1)

    cstr_type = {
        "CS_MSO": "Start On", 
        "CS_MSOB": "Start On or Before", 
        "CS_MSOA": "Start On or After",
        "CS_MEO": "Finish On", 
        "CS_MEOB": "Finish On or Before", 
        "CS_MEOA": "Finish On or After", 
        "CS_ALAP": "As Late as Possible", 
        "CS_MANDSTART": "Mandatory Start", 
        "CS_MANDFIN": "Mandatory Finish", 
    }
    df_qualidade['Constraints'] = df_qualidade.apply(lambda row: cstr_type[row['cstr_type']] if row['cstr_date'] else 'ok', axis=1)

    def _analise_duracao(row):
        if row['status_code'] == "Complete":
            return "Atividade Finalizada"
        elif "Mile" in row['task_type']:
            return "Milestone"
        elif row['remain_drtn_days'] <= 2*7:
            return "0 Semanas a 2 Semanas"
        elif row['remain_drtn_days'] <= 1*30:
            return "2 Semanas a 1 Mês"
        elif row['remain_drtn_days'] <= 2*30:
            return "1 Mês a 2 Meses"
        elif row['remain_drtn_days'] <= 3*30:
            return "2 Meses a 3 Meses"
        elif row['remain_drtn_days'] <= 6*30:
            return "3 Meses a 6 Meses"
        elif row['remain_drtn_days'] <= 1*365:
            return "6 Meses a 1 Ano"
        elif row['remain_drtn_days'] <= 2*365:
            return "1 Ano a 2 Anos"
        else:
            return "Mais que 2 Anos"

    df_qualidade['Analise_Duracao_Remanescente'] = df_qualidade.apply(_analise_duracao, axis=1)

    def _analise_folga(row):
        if row['status_code'] == "Complete":
            return "Atividade Finalizada"
        elif row['total_float_days'] <= 10:
            return "Folga <= 10 dias"
        elif row['total_float_days'] >= ((row['termino_projeto'] - row['last_recalc_date']).days * 0.25):
            return "Folga >= 25% Duração Remanescente"
        else:
            return "Atividades Balanceadas"

    df_qualidade['Analise_Folga'] = df_qualidade.apply(_analise_folga, axis=1)


    def _analise_longa_duracao(row):
        if row['target_end_date'] - row['target_start_date'] <= 0:
            return "0 dias"
        elif row['target_end_date'] - row['target_start_date'] <= 50:
            return "50 dias"
        elif row['target_end_date'] - row['target_start_date'] <= 100:
            return "100 dias"
        elif row['target_end_date'] - row['target_start_date'] <= 200:
            return "200 dias"
        else:
            return "Mais de 200 dias"
        
    df_qualidade['Longa_Duracao'] = df_qualidade.apply(_analise_folga, axis=1)
    df_qualidade['Qualidade_Logica'] = df_qualidade['Total_Links'].apply(lambda x: "Sem link Lógico" if x == 0 else 'ok')

    def _Qualidade_Densidade_Logica(x):
        if x < 2:
            return "Menos de 2 Links"
        elif x < 6:
            return "Entre 2 e 6 Links"
        else:
            return "Mais de 6 Links"

    df_qualidade['Qualidade_Densidade_Logica'] = df_qualidade['Total_Links'].apply(_Qualidade_Densidade_Logica)


    df_qualidade['Qualidade_Restricoes_Duras'] = df_qualidade['Constraints'].apply(lambda x: "Possui Restrição Dura" if x in ['Mandatory Start', 'Mandatory Finish'] else 'ok')
    df_qualidade['Qualidade_Folga_Negativa'] = df_qualidade['total_float_days'].apply(lambda x: "Folga Negativa" if x < 0 else 'ok')
    df_qualidade['Qualidade_Numero_Leads'] = df_qualidade['lag_days_menor_zero'].apply(lambda x: "Links com lag < 0 dias" if x > 0 else 'ok')
    df_qualidade['Qualidade_Hotspot_Mesclagem'] = df_qualidade['Quant_Predecessoras'].apply(lambda x: "Mais de 10 Predecessoras" if x > 10 else 'ok')

    def _folga_positiva(x):
        folgas = [0, 30, 60, 90, 150, 200]
        for idx, folga in enumerate(folgas):
            if x < folga:
                if idx == 0:
                    return 'Folga Menor ou Igual a 0 Dias'
                else:
                    return f'Folga entre {folgas[idx-1]} e {folga} Dias'
        return "Folga Maior ou Igual a 200 Dias"
                
    df_qualidade['Qualidade_Folga_Positiva'] = df_qualidade['total_float_days'].apply(_folga_positiva)
    df_qualidade['ID_Projeto'] = projeto_id
    df_qualidade['ID_Arquivo'] = execucao_id
    print('Uploading table: Consistencia_Qualidade')
    df_qualidade[_get_table_columns('Consistencia_Qualidade', cnxn,'Cronograma_Master')].to_sql(
        'Consistencia_Qualidade',
        schema='Cronograma_Master',
        con=engine,
        if_exists='append',
        index=False
    )
    # df_qualidade[TableColumns.df_qualidade].to_parquet(
    #     os.path.join(output_path, 'df_qualidade.parquet'),
    #     index=False
    # )
    #####################################################################################################
    print('Starting pipeline: Fora_Sequencia')
    df_fora_squencia = pd.merge(
        df_predecessora,
        df_atividades[['task_id','status_code','data_start','data_end',]],
        how='left',
        on='task_id'
    )

    df_fora_squencia['data_start'] = pd.to_datetime(df_fora_squencia['data_start'])
    df_fora_squencia['data_end'] = pd.to_datetime(df_fora_squencia['data_end'])
    df_fora_squencia['pred.data_start'] = pd.to_datetime(df_fora_squencia['pred.data_start'])
    df_fora_squencia['pred.data_end'] = pd.to_datetime(df_fora_squencia['pred.data_end'])

    def _fs(row):
        if row['pred_type'] == "PR_FS":
            if (row['status_code'] == "In Progress" or row['status_code'] == "Complete") and (row['pred.status_code'] != "Complete") and (row['data_start'] > (row['pred.data_end'] + dt.timedelta(days=row['lag_days']))):
                return 'Inconsistente'
        return None
        
    def _ff(row):
        if row['pred_type'] == "PR_FF":
            if (row['status_code'] == "Complete" and row['pred.status_code'] != "Complete"):
                return 'Inconsistente'
        return None

    def _sf(row):
        if row['pred_type'] == "PR_SF":
            if (row['status_code'] == "Complete" and row['pred.status_code'] == "Not Started"):
                return 'Inconsistente'
        return None 

    def _ss(row):
        if row['pred_type'] == "PR_SS":
            if (row['status_code'] != "Not Started" and row['pred.status_code'] == "Not Started" and row['data_start'] > (row['pred.data_end'] + dt.timedelta(days=row['lag_days']))):
                return 'Inconsistente'
        return None 

    df_fora_squencia['FS'] = df_fora_squencia.apply( _fs, axis=1)
    df_fora_squencia['FF'] = df_fora_squencia.apply( _ff, axis=1)
    df_fora_squencia['SF'] = df_fora_squencia.apply( _sf, axis=1)
    df_fora_squencia['SS'] = df_fora_squencia.apply( _ss, axis=1)
    df_fora_squencia['Chave_task_pred_id'] = df_fora_squencia['ID_Arquivo'].astype(str) + '_' + df_fora_squencia['task_pred_id'].astype(str)

    df_fora_squencia = pd.melt(
        df_fora_squencia,
        id_vars=['ID_Arquivo', 'ID_Projeto', 'Chave_task_pred_id'],
        value_vars=['FS', 'FF', 'SF', 'SS'],
        var_name='Sequencia',
        value_name='Valor'
    ).dropna()
    print('Uploading table: Fora_Sequencia')
    df_fora_squencia[_get_table_columns('Fora_Sequencia', cnxn,'Cronograma_Master')].to_sql(
        'Fora_Sequencia',
        schema='Cronograma_Master',
        con=engine,
        if_exists='append',
        index=False
    )
    # df_fora_squencia[TableColumns.df_fora_squencia].to_parquet(
    #     os.path.join(output_path, 'df_fora_squencia.parquet'),
    # )

    ######################################################################################################
    print('Starting pipeline: Codigos')
    df_actvcode = xer_parser.render_table('ACTVCODE')
    df_actvtype = xer_parser.render_table('ACTVTYPE')
    df_taskactv = xer_parser.render_table('TASKACTV')
    column_names = {
        'udf_type_label':'actv_code_type ',
        'udf_type_name':'actv_code_name ',
        'fk_id': 'task_id',
    }
    
    df_codigos = pd.merge(
        df_taskactv,
        df_actvtype,
        on='actv_code_type_id',
        how='left'
    )
    df_codigos = pd.merge(
        df_codigos,
        df_actvcode,
        on='actv_code_id',
        how='left'
    )
    try:
        df_udftype = xer_parser.render_table('UDFTYPE')
        df_udfvalue = xer_parser.render_table('UDFVALUE')
        df_udf = pd.merge(
            df_udfvalue,
            df_udftype,
            on='udf_type_id',
            how='left'
        ).rename(columns=column_names)[column_names.values()]
        df_codigos = pd.merge(
            df_codigos,
            df_udf,
            on='task_id',
            how='left'
        ).dropna(subset=['actv_code_type']).rename(columns={'short_name': 'actv_code_value'})
    except:
        pass
    

    df_codigos['actv_code_complete'] = df_codigos['actv_code_value'] + '_' + df_codigos['actv_code_name']
    df_codigos['ID_Projeto'] = projeto_id
    df_codigos['ID_Arquivo'] = execucao_id
    df_codigos['Chave_task_id'] = str(execucao_id) + '_' + df_codigos['task_id']
    df_codigos[_get_table_columns('Codigos', cnxn,'Cronograma_Master')].to_sql(
        'Codigos',
        schema='Cronograma_Master',
        con=engine,
        if_exists='append',
        index=False
    )
    # df_codigos[TableColumns.df_codigos].to_parquet(
    #     os.path.join(output_path, 'df_codigos.parquet'),
    # )



def _to_usd(file_contents):
    p = re.compile('(\d)[,](\d)')
    return p.sub(r'\1.\2', file_contents)


def _xer_loader(xer_path):
    response = requests.get(xer_path)

    if response.status_code == 200:
        # Salva o conteúdo do blob em um arquivo temporário
        with BytesIO(response.content) as f:
            file_contents = f.read().decode('cp1252', errors='ignore')
    'UTF-8'
    'cp1252'


    try:
        return Xer(file_contents)
    except:
        return Xer(_to_usd(file_contents))


def _get_table_columns(table_name, cnxn,schema=None):
    query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table_name}'"
    if schema:
        query += f"AND TABLE_SCHEMA = N'{schema}'"
    return [column[0] for column in cnxn.execute(query)]
