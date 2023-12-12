import xlsxwriter as xls
import pandas as pd

def verifica_valor(valor):
    if pd.isna(valor):
        return None
    else:
        return valor

def formata_data(data):
    try:
        data = data.strftime("%d/%m/%Y %H:%M")
    except:
        data = None

    return data


def retorna_registro_contratada(OP, avancos):
    linha = avancos.loc[avancos['OP_WP'] == OP]

    if not linha.empty:
       print(linha['avanco'])
       soma_previsto = linha['previsto'].sum()
       print(soma_previsto)
       soma_real = linha['actual'].sum()
       print(soma_real)
       try:
            avanco = soma_real/soma_previsto
       except:
            avanco = 0
       menor_data_inicio_real = linha['data_inicio_real'].dropna().min()
       if avanco < 1:
        maior_data_fim_real = None
       else:
        maior_data_fim_real = linha['data_fim_real'].dropna().max()

       valores = [avanco, menor_data_inicio_real,  maior_data_fim_real]

    else:
        valores = None

    return valores



def criar_planilha_avanco(output, tasks, recursos, avancos):
    wb = xls.Workbook(output)

    task_planilha = wb.add_worksheet("TASK")  # BD
    taskrsrc_planilha = wb.add_worksheet("TASKRSRC")  # BD
    userdata = wb.add_worksheet("USERDATA")  # User

    dict_avanco = {}

    planilha_task(task_planilha, tasks, avancos, wb, dict_avanco)
    planilha_taskrsrc(taskrsrc_planilha, recursos, avancos, wb, dict_avanco)
    planilha_userdata(userdata, wb)


    wb.close()


def planilha_task(task_planilha, tasks, avancos, wb, dict_avanco):

    task_planilha.write_row(0, 0, ['task_code', 'status_code', 'wbs_id', 'actv_code_op_cwp_501_id', 'task_name', 'complete_pct', 'act_start_date', 'act_end_date', 'delete_record_flag'])
    task_planilha.write_row(1, 0, ['Activity ID', 'Activity Status', 'WBS Code', 'OP_CWP', 'Activity Name', 'Activity % Complete(%)', 'Actual Start', 'Actual Finish', 'Delete This Row'])
    formato_percentual = wb.add_format({'num_format': '0.00%'})
    formato_data = wb.add_format({'num_format': 'dd/mm/yyyy'})
    row_num = 2

    for task in tasks:


        task_planilha.write(row_num, 1, task.activity_status)
        task_planilha.write(row_num, 2, task.wbs_code)
        task_planilha.write(row_num, 3, task.op_cwp)
        task_planilha.write(row_num, 4, task.activity_name)
        valores = retorna_registro_contratada(task.op_cwp, avancos)
        print(valores)
        if valores:
            try:
                task_planilha.write(row_num, 5, valores[0], formato_percentual)
                dict_avanco[task.activity_id] = valores[0]
            except:
                task_planilha.write(row_num, 5, None, formato_percentual)
                dict_avanco[task.activity_id] = 0
            try:
                task_planilha.write(row_num, 6, valores[1], formato_data)
            except:
                task_planilha.write(row_num, 6, None)
            try:
                task_planilha.write(row_num, 7, valores[2], formato_data)
            except:
                task_planilha.write(row_num, 7, None)


        row_num += 1

    task_planilha.set_column('A:A', 21.86)
    task_planilha.set_column('B:B', 13.00)
    task_planilha.set_column('C:C', 20.14)
    task_planilha.set_column('D:D', 31.57)
    task_planilha.set_column('E:E', 118.57)
    task_planilha.set_column('F:F', 21.57)
    task_planilha.set_column('G:G', 15.14)
    task_planilha.set_column('H:H', 15.14)
    task_planilha.set_column('I:I', 17.43)


def planilha_taskrsrc(taskrsrc_planilha, recursos, avancos, wb, dict_avanco):

    taskrsrc_planilha.write_row(0, 0, ['rsrc_id', 'task_id', 'TASK__status_code', 'role_id', 'acct_id', 'target_qty', 'act_qty', 'target_cost', 'act_cost', 'delete_record_flag'])
    taskrsrc_planilha.write_row(1, 0, ['Resource ID', 'Activity ID', '(*)Activity Status', 'Role ID', 'Cost Account ID','Budgeted Units(h)', 'Actual Units(h)', 'Budgeted Cost', 'Actual Cost', 'Delete This Row'])

    row_num = 2

    for recurso in recursos:
        taskrsrc_planilha.write(row_num, 0, recurso.rsrc_id)
        taskrsrc_planilha.write(row_num, 1, recurso.activity_id)
        taskrsrc_planilha.write(row_num, 2, recurso.task_status_code)
        taskrsrc_planilha.write(row_num, 3, recurso.role_id)
        taskrsrc_planilha.write(row_num, 4, recurso.acct_id)
        taskrsrc_planilha.write(row_num, 5, recurso.target_qty)
        try:
            taskrsrc_planilha.write(row_num, 6, dict_avanco[recurso.activity_id] * recurso.target_qty)
        except:
            pass

        row_num += 1

    taskrsrc_planilha.set_column('A:A', 27.71)
    taskrsrc_planilha.set_column('B:B', 17.71)
    taskrsrc_planilha.set_column('C:C', 20.57)
    taskrsrc_planilha.set_column('D:D', 19.29)
    taskrsrc_planilha.set_column('E:E', 19.29)
    taskrsrc_planilha.set_column('F:F', 19.29)
    taskrsrc_planilha.set_column('G:G', 19.29)
    taskrsrc_planilha.set_column('H:H', 19.29)
    taskrsrc_planilha.set_column('I:I', 19.29)
    taskrsrc_planilha.set_column('J:J', 19.29)



def planilha_userdata(userdata, wb):

    userdata.write_row(0, 0, ['user_data'])
    userdata.write_row(1, 0, ['UserSettings Do Not Edit'])
    userdata.write_row(2, 0, ['DurationQtyType=QT_Day ShowAsPercentage=0 SmallScaleQtyType=QT_Hour'])


