import pandas as pd
from xerparser.src.xer import Xer
from datetime import datetime
import re
import datetime as dt
import time


class CurvaRecursos:
    _date_format = '%d/%m/%y'

    _columns = {
        'Activity ID': 'task_code',
        'Resource Name': 'rsrc_name',
        'Resource Type': 'rsrc_type',
        'Spreadsheet Field': 'spreadsheet_field',
    }

    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def get_table(self):
        self._read_file()
        self._transform()
        return self.df

    def _read_file(self):
        self.df_raw = pd.read_excel(
            self.file_path,
            na_values=[' A']
        )

    def _transform(self):
        df = self.df_raw
        df = df.rename(columns=self._columns)

        date_columns = [column for column in df.columns if isinstance(column, dt.datetime)]
        id_columns = [column for column in df.columns if column in self._columns.values()]
        df = pd.melt(
            df,
            id_vars=id_columns,
            value_vars=date_columns,
            var_name='date',
            value_name='worked_units',
        )

        df = df.dropna(subset=['worked_units'])
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        df['worked_units'] = df['worked_units'].astype(float)
        self.df = df


class Calendars:
    def __init__(self, xer, start_date=(2022, 2, 1), end_date=(2025, 12, 30)) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.xer = xer
        self.rendered_calendars = {}
        xer_tables = XerTableRender(xer.tables)
        self.calendar_table = xer_tables.render_table('CALENDAR').set_index('clndr_id')

    def calculate_worked_days(self, id):
        calendar = self._render_calendar(id)
        return calendar

    def pre_render_calendars(self):
        for calendar_id in self.xer.calendars.keys():
            self._render_calendar(calendar_id)

    def _render_calendar(self, id):
        if id:
            [records] = self.calendar_table.loc[[id]].to_dict(orient='records')
            calendar = Calendar(self.xer.calendars[id], records)
            calendar = calendar.load_tables(self.start_date, self.end_date)
            base_clndr_id = calendar.calendar.base_clndr_id
            base_clndr = self.rendered_calendars.get(base_clndr_id)
            base_clndr = base_clndr if base_clndr else self._render_calendar(base_clndr_id)
            calendar = calendar.transform(base_clndr)
            self.rendered_calendars[id] = calendar
            return calendar
        else:
            return None


class Calendar:
    def __init__(self, calendar, *missing_args) -> None:
        self.calendar = calendar
        for dictionary in missing_args:
            for key in dictionary:
                setattr(self, key, dictionary[key])

    def calculate_worked_days(self, start, end):
        worked_days = self.calendar_table.loc[
            (self.calendar_table['shift_end'] >= start) &
            (self.calendar_table['shift_start'] <= end)
            ]

        worked_days.loc[
            (worked_days['date'].dt.date == start.date()) &
            (start > self.calendar_table['shift_start']),
            ['shift_start']
        ] = start
        worked_days.loc[
            (worked_days['date'].dt.date == end.date()) &
            (end < self.calendar_table['shift_end']),
            ['shift_end']
        ] = end
        worked_days['worked_hrs'] = (worked_days['shift_end'] - worked_days['shift_start']).dt.total_seconds() / (
                    60 * 60)  # convert seconds to hours
        worked_days['worked_days'] = worked_days['worked_hrs'] / worked_days['day_hr_cnt']
        self.worked_days = worked_days
        return self.worked_days

    def load_tables(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.work_days = pd.DataFrame(
            {'date': self.calendar.iter_workdays(dt.datetime(*self.start_date), dt.datetime(*self.end_date))})
        self.holidays = pd.DataFrame({'date': self.calendar.holidays})
        self.exception = pd.DataFrame([
            (day, *shift)
            for day, values in self.calendar.work_exceptions.items()
            for shift in values.shifts
        ], columns=['date', 'shift_start', 'shift_end'])

        self.work_week = pd.DataFrame([
            (time.strptime(weekday, "%A").tm_wday, *shift)
            for weekday, values in self.calendar.work_week.items()
            for shift in values.shifts
        ], columns=['dayofweek', 'shift_start', 'shift_end'])
        return self

    def transform(self, base_clndr=None):

        df = self.work_days
        df['dayofweek'] = pd.to_datetime(df['date']).dt.dayofweek
        df = pd.merge(
            df,
            self.work_week,
            on=['dayofweek'],
            how='left'
        )

        df_work_exceptions = self.exception.loc[self.exception['date'].isin(df['date'])]
        df = df.loc[~df['date'].isin(df_work_exceptions['date'])]

        if base_clndr:
            df = df.loc[~df['date'].isin(base_clndr.holidays['date'])]

        if not df_work_exceptions.empty:
            df = pd.concat([df, df_work_exceptions], axis=0).reset_index(drop=True)

        df['shift_start'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['shift_start'].astype(str))
        df['shift_end'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['shift_end'].astype(str))
        df.loc[df['shift_end'] == df['shift_start'], 'shift_end'] = df['shift_end'] + dt.timedelta(days=1)
        df['day_hr_cnt'] = float(self.day_hr_cnt)
        self.calendar_table = df.drop(columns=['dayofweek'])
        return self


class XerTableRender:
    datetime_format = '%Y-%m-%d %H:%M'

    def __init__(self, tables) -> None:
        self.tables = tables

    def render_table(self, table_name):
        table = self._default_transform(pd.DataFrame(self.tables[table_name]))
        return getattr(self, f'_{table_name.lower()}')(table)

    def _default_transform(self, df_table):
        df_table = df_table.replace(r'^\s*$', None, regex=True)

        return df_table

    def _task(self, df_table):
        datetime_cols = [
            'act_start_date',
            'act_end_date',
            'restart_date',
            'reend_date',
            'early_start_date',
            'early_end_date',
            'target_start_date',
            'target_end_date',
        ]
        numeric_cols = [
            'total_float_hr_cnt',
            'free_float_hr_cnt',
            'remain_drtn_hr_cnt',
            'target_drtn_hr_cnt',
            'phys_complete_pct',
        ]

        # df_table[numeric_cols] = df_table[numeric_cols].map(self._optional_float_value)
        df_table[numeric_cols] = df_table[numeric_cols].astype(float)
        df_table[datetime_cols] = df_table[datetime_cols].map(
            lambda x: dt.datetime.strptime(x, self.datetime_format) if x else x)

        df_table['start_date'] = df_table['act_start_date']
        df_table.loc[df_table['start_date'].isna(), 'start_date'] = df_table['restart_date']
        df_table.loc[df_table['start_date'].isna(), 'start_date'] = df_table['early_start_date']
        df_table.loc[df_table['start_date'].isna(), 'start_date'] = df_table['target_start_date']
        df_table['start_date'] = pd.to_datetime(df_table['start_date'])



        df_table['end_date'] = df_table['act_end_date']
        df_table.loc[df_table['end_date'].isna(), 'end_date'] = df_table['reend_date']
        df_table.loc[df_table['end_date'].isna(), 'end_date'] = df_table['early_end_date']
        df_table.loc[df_table['end_date'].isna(), 'end_date'] = df_table['target_end_date']
        df_table['end_date'] = pd.to_datetime(df_table['end_date'])
        try:
            df_table['Start'] = df_table['start_date'].dt.strftime('%d/%m/%Y') + ' A'
        except:
            df_table['Start'] = df_table['start_date'].dt.strftime('%d/%m/%Y')
        try:
            df_table['Finish'] = df_table['end_date'].dt.strftime('%d/%m/%Y') + ' A'
        except:
            df_table['Finish'] = df_table['end_date'].dt.strftime('%d/%m/%Y')

        df_table.loc[~df_table['act_start_date'].isna(), 'Start'] = df_table['act_start_date']
        df_table.loc[~df_table['act_end_date'].isna(), 'Finish'] = df_table['act_end_date']

        df_table.loc[df_table['status_code'] == 'TK_Active', 'status_code'] = 'In Progress'
        df_table.loc[df_table['status_code'] == 'TK_NotStart', 'status_code'] = 'Not Started'
        df_table.loc[df_table['status_code'] == 'TK_Complete', 'status_code'] = 'Complete'

        df_table['total_float_hr_cnt'] == df_table['total_float_hr_cnt'].astype(float)
        df_table['free_float_hr_cnt'] == df_table['free_float_hr_cnt'].astype(float)
        return df_table

    def _taskrsrc(self, df_table):
        numeric_cols = [
            'act_reg_qty',
            'act_ot_qty',
            'remain_qty'
        ]
        df_table[numeric_cols] = df_table[numeric_cols].astype(float)
        df_table['act_total_qty'] = df_table['act_reg_qty'] + df_table['act_ot_qty']
        df_table['at_completion_qty'] = df_table['act_total_qty'] + df_table['remain_qty']
        return df_table

    def _rsrccurvdata(self, df_table):
        pct_usage_columns = [f'pct_usage_{idx}' for idx in range(21)]
        df_table['curv_pct'] = df_table[pct_usage_columns].values.tolist()
        df_table = df_table.drop(columns=pct_usage_columns)
        return df_table

    def _calendar(self, df_table):
        numeric_cols = [
            'day_hr_cnt',
        ]
        df_table[numeric_cols] = df_table[numeric_cols].astype(float)
        return df_table

    def _project(self, df_table):
        datetime_cols = [
            'last_recalc_date',
        ]
        df_table[datetime_cols] = df_table[datetime_cols].map(
            lambda x: dt.datetime.strptime(x, self.datetime_format) if x else x)
        return df_table

    def _taskpred(self, df_table):
        numeric_cols = [
            'lag_hr_cnt',
        ]
        df_table[numeric_cols] = df_table[numeric_cols].astype(float)
        return df_table

    def _udfvalue(self, df_table):
        return df_table

    def _udftype(self, df_table):
        return df_table

    def _actvcode(self, df_table):
        return df_table

    def _actvtype(self, df_table):
        return df_table

    def _taskactv(self, df_table):
        return df_table




def _to_usd(file_contents):
    p = re.compile('(\d)[,](\d)')
    return p.sub(r'\1.\2', file_contents)

def _xer_loader(xer_path):
    with open(xer_path, encoding='cp1252', errors="ignore") as f:
        file_contents = f.read()
    try:
        return Xer(file_contents)
    except:
        return Xer(_to_usd(file_contents))




def cria_df_carga_xer(xer_parser, ow_wp, ponderacao):
    df_actvcode = xer_parser.render_table('ACTVCODE')
    df_actvtype = xer_parser.render_table('ACTVTYPE')
    df_udftype = xer_parser.render_table('UDFTYPE')
    df_udfvalue = xer_parser.render_table('UDFVALUE')
    df_taskactv = xer_parser.render_table('TASKACTV')
    df_task = xer_parser.render_table('TASK')

    df_actvtype = df_actvtype.loc[df_actvtype['actv_code_type'] == ow_wp]

    column_names = {
        'udf_type_label': 'actv_code_type ',
        'udf_type_name': 'actv_code_name ',
        'fk_id': 'task_id',
    }

    df_udf = pd.merge(
        df_udfvalue,
        df_udftype,
        on='udf_type_id',
        how='left'
    ).rename(columns=column_names)[column_names.values()]

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

    df_codigos = pd.merge(
        df_codigos,
        df_udf,
        on='task_id',
        how='left'
    ).dropna(subset=['actv_code_type']).rename(columns={'short_name': 'actv_code_value'})

    df_carga = pd.merge(
        df_task,
        df_codigos,
        on='task_id',
        how='left'
    )

    df_carga.to_excel('df_antes_tratado.xlsx')
    print(ponderacao)
    print(ponderacao)
    print(ponderacao)
    print(ponderacao)

    if ponderacao == '2':
        coluna_previsto = 'target_equip_qty'
        coluna_real = 'act_equip_qty'
    else:
        coluna_previsto = 'target_work_qty'
        coluna_real = 'act_work_qty'

    valores = {
               'task_code': 'ID',
               'task_name': 'Descrição',
               'free_float_hr_cnt': 'Folga Livre',
               'total_float_hr_cnt': 'Folga Total',
               'target_drtn_hr_cnt': 'Duração',
               'phys_complete_pct': 'Avanço',
               'target_start_date': 'Data Início BL',
               'target_end_date': 'Data Fim BL',
               'restart_date': 'Data Início Reprogramado',
               'reend_date': 'Data Fim Reprogramado',
               'act_start_date': 'Data Início Real',
               'act_end_date': 'Data Fim Real',
               coluna_previsto: 'previsto',
               coluna_real: 'actual',
               'actv_code_value': 'OP_WP',

               }



    df_carga = df_carga[valores.keys()].rename(columns=valores)

    df_carga.to_excel('df_tratado.xlsx')

    return df_carga