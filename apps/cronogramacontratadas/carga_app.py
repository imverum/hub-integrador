import pandas as pd
from xerparser.src.xer import Xer
from datetime import datetime
import re
import datetime as dt
from sqlalchemy import create_engine, text
import pyodbc
from apps.core.tratar_datas import tratar_data
from apps.cronogramacontratadas.carga_xer import XerTableRender, _xer_loader


def carga_app(file_path):
    xer = _xer_loader(file_path)
    xer_parser = XerTableRender(xer.tables)

    df_actvcode = xer_parser.render_table('ACTVCODE')
    df_actvtype = xer_parser.render_table('ACTVTYPE')
    df_taskactv = xer_parser.render_table('TASKACTV')
    df_task = xer_parser.render_table('TASK')

    column_names = {
        'udf_type_label': 'actv_code_type ',
        'udf_type_name': 'actv_code_name ',
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
    df_carga = pd.merge(
        df_task,
        df_codigos,
        on='task_id',
        how='left'
    )
    df_pivotado = df_carga.pivot_table(values='short_name', index=df_carga.task_id, columns='actv_code_type',
                                       aggfunc='first')
    df_carga = pd.merge(
        df_carga,
        df_pivotado,
        on='task_id',
        how='left'
    )

    return df_carga


def etl_pandas_xer(df_carga):
    df_carga['start_date'] = df_carga['start_date'].dt.strftime('%Y-%m-%d')
    df_carga['end_date'] = df_carga['end_date'].dt.strftime('%Y-%m-%d')

    df_carga = df_carga[['task_code', 'status_code', 'task_name', 'start_date', 'end_date','AC02 - CWA' ,'AC03 - DISCIPLINA', 'AC04 - SUBDISCIPLINA',
                         'AC05 - SUB-ÁREA', 'AC06 - CWP',  'AC07 - EWPc',  'AC08 - PWPe', 'phys_complete_pct',
                         'AC09 - PWPp', 'AC10 - PWPl', 'AC11 - SWP','total_float_hr_cnt']]

    df_carga['CWP'] = df_carga['AC06 - CWP'].combine_first(
        df_carga['AC07 - EWPc']).combine_first(
        df_carga['AC08 - PWPe']).combine_first(
        df_carga['AC09 - PWPp']).combine_first(
        df_carga['AC10 - PWPl']).combine_first(
        df_carga['AC11 - SWP'])

    df_carga = df_carga.rename(columns={
        'task_code': 'Code',
        'status_code': 'Status',
        'task_name': 'Atividade',
        'start_date': 'Inicio_BL1',
        'end_date': 'Fim_BL1',
        'AC02 - CWA': 'Area',
        'CWP': 'CWP',
        'AC03 - DISCIPLINA': 'Disciplina',
        'AC05 - SUB-ÁREA': 'SubArea',
        'phys_complete_pct': 'Avanco',
        'AC04 - SUBDISCIPLINA': 'Subdisciplina',
        'total_float_hr_cnt': 'Folga'
    })

    colunas_renomeadas = [
        'Code',
        'Status',
        'Atividade',
        'Inicio_BL1',
        'Fim_BL1',
        'Area',
        'CWP',
        'Disciplina',
        'SubArea',
        'Avanco',
        'Subdisciplina',
        'Folga'
    ]

    todas_colunas = df_carga.columns
    colunas_para_excluir = [coluna for coluna in todas_colunas if coluna not in colunas_renomeadas]

    df_carga = df_carga.drop(columns=colunas_para_excluir)

    df_carga['Avanco'] = df_carga['Avanco'] / 100

    df_carga["Folga"] = df_carga["Folga"].apply(lambda resource_name: None if pd.isna(resource_name) else resource_name)

    df_carga = df_carga.drop_duplicates(subset='Code')
    df_carga = df_carga[df_carga['CWP'].notna()]

    return df_carga

def carga_dados_banco(df_carga):
    try:
        conn_str = (

            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=onca-puma.database.windows.net;"
            "Database=app_construcao;"
            "uid=app_construcao;"
            "pwd=3MpHQd13FMxYIyn"
        )

        #cnxn = pyodbc.connect(conn_str)
        engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn_str))
        # Especificar o esquema (schema) na tabela
        tabela = 'atividade'
        esquema = 'dbo'
        nome_completo_tabela = f'[{esquema}].[{tabela}]'


        for index, row in df_carga.iterrows():
            code = row['Code']

            # Criar uma lista de atualizações tratando tipos de dados e NaN
            updates = []

            consulta_existencia = f"SELECT COUNT(*) FROM atividade_homolog WHERE Code = '{code}'"
            with engine.connect() as con:
                resultado_existencia = con.execute(text(consulta_existencia)).scalar()

            if resultado_existencia > 0:
                for key, value in row.items():
                    if key != 'Code':
                        if pd.isna(value):
                            updates.append(f"{key} = NULL")
                        elif isinstance(value, str):
                            updates.append(f"{key} = '{value}'")
                        else:
                            updates.append(f"{key} = {value}")

                update_values = ", ".join(updates)

                consulta_sql = f"""
                    UPDATE {nome_completo_tabela}
                    SET {update_values}
                    WHERE Code = '{code}'
                """
                # Use text() para criar um objeto text representando a consulta SQL
                consulta_text = text(consulta_sql)
                try:
                    with engine.connect() as con:
                        con.execute(consulta_text)
                        con.commit()
                except Exception as e:
                    print(e)
            else:
                # Inserir um novo registro se ele não existir
                colunas = ', '.join([f"[{col}]" for col in row.index])
                valores = ', '.join([f"'{str(val)}'" if not pd.isna(val) else 'NULL' for val in row.values])

                consulta_sql = f"""
                    INSERT INTO {nome_completo_tabela} ({colunas})
                    VALUES ({valores})
                """

                # Use text() para criar um objeto text representando a consulta SQL
                consulta_text = text(consulta_sql)
                try:
                    with engine.connect() as con:
                        con.execute(consulta_text)
                        con.commit()
                except Exception as e:
                    print(e)
    except:
        pass