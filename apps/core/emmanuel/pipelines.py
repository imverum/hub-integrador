from sqlalchemy import create_engine
from render import Calendars, XerTableRender
from xerparser import Xer
from xer import CurvaRecursos
import re
import pandas as pd
import pyodbc 
import math
import os



conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=onca-puma.database.windows.net;"
    "Database=DB_Verum_IPE;"
    "uid=emmanuelsantana;"
    "pwd=Recife@2023"
)
# cnxn = pyodbc.connect(conn_str)
# engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn_str))

projeto_id = 2
execucao_id = 0



def _to_usd(file_contents):
    p = re.compile('(\d)[,](\d)')
    return p.sub(r'\1.\2', file_contents)


def _xer_loader(xer_path):
    with open(xer_path, encoding=Xer.CODEC, errors="ignore") as f:
            file_contents = f.read()
    try:
        return Xer(file_contents)
    except:
        return Xer(_to_usd(file_contents))


def get_baseline_table(xer_path):    
    start_date = (2022, 2, 1)
    end_date = (2025, 12, 30)


    xer =_xer_loader(xer_path)
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
    df_worked_days['duracao_original'] = df_worked_days['worked_days'].apply(lambda x: math.floor(x) if (x % 1) < 0.5 else math.ceil(x))    
    df_baseline = pd.merge(
        df_baseline,
        df_worked_days.drop_duplicates(subset=['task_code']),
        on='task_code',
        how='left'
    ).fillna(0)

    df_baseline = df_baseline.drop(columns=['clndr_id'])
    return df_baseline