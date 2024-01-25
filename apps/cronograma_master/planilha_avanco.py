import xlsxwriter as xls
import pandas as pd

def retorna_validacao_dados(task,avancos):
    linha = avancos.loc[avancos['OP_WP'] == task.op_cwp]

    contratada_inicio_reprogramda = linha['data_inicio_reprogramada'].dropna().min()
    contratada_termino_reprogramda = linha['data_fim_reprogramada'].dropna().max()

    return [task.act_start_date, contratada_inicio_reprogramda, task.start_date, task.act_end_date,contratada_termino_reprogramda, task.end_date, task.op_cwp, task.activity_id]

def verifica_datas_reprogramadas(avancos, tasks, df):
    #df = pd.DataFrame(columns=['OP_atividade', 'task_code', 'data', 'valor CR contratada', 'valor CR master'])

    for task in tasks:
        master_inicio_real, contratada_inicio_reprogramda, master_inicio_reprogramda,master_termino_real, contratada_termino_reprogramda, master_termino_reprogramda, OP_atividade, task_code= retorna_validacao_dados(task,avancos)

        if not master_inicio_real:
            if contratada_inicio_reprogramda != master_inicio_reprogramda:
                df.loc[len(df)] = [OP_atividade, task_code, 'início reprogramda', contratada_inicio_reprogramda, master_inicio_reprogramda]

        if not master_termino_real:
            if contratada_termino_reprogramda != master_termino_reprogramda:
                df.loc[len(df)] = [OP_atividade, task_code, 'termino reprogramda', contratada_termino_reprogramda, master_termino_reprogramda]

    return df



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


def retorna_registro_contratada(OP, complete_pct,avancos):
    linha = avancos.loc[avancos['OP_WP'] == OP]
    if complete_pct == None:
        complete_pct = 0
    else:
        complete_pct = float(complete_pct)

    if not linha.empty:
       print(linha['avanco'])
       soma_previsto = linha['previsto'].sum()
       print(soma_previsto)
       soma_real = linha['actual'].sum()
       print(soma_real)
       try:
            avanco = soma_real/soma_previsto
            if avanco <= complete_pct:
                return None
       except:
            return None

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

    task_planilha.write_row(0, 0, ['task_code', 'status_code', 'wbs_id', 'task_name', 'target_drtn_hr_cnt','complete_pct', 'start_date', 'end_date',  'act_start_date', 'act_end_date', 'actv_code_op_cwp_4635_id', 'actv_code_op_pacote_de_suprimentos_4635_id','delete_record_flag'])
    task_planilha.write_row(1, 0, ['Activity ID', 'Activity Status', 'WBS Code', 'Activity Name', 'Original Duration(d)', 'Activity % Complete(%)', '(*)Start', '(*)Finish', 'Actual Start', 'Actual Finish', 'OP_CWP',  'OP_PACOTE DE SUPRIMENTOS',  'Delete This Row'])

    formato_percentual = wb.add_format({'num_format': '0.00%'})
    formato_data = wb.add_format({'num_format': 'dd/mm/yyyy'})
    row_num = 2

    for task in tasks:



        valores = retorna_registro_contratada(task.op_cwp, task.complete_pct,avancos)
        print(valores)
        if valores:
            task_planilha.write(row_num, 0, task.activity_id)
            task_planilha.write(row_num, 1, task.activity_status)
            task_planilha.write(row_num, 2, task.wbs_code)
            task_planilha.write(row_num, 3, task.activity_name)
            task_planilha.write(row_num, 4, task.target_drtn_hr_cnt)
            task_planilha.write(row_num, 6, task.start_date)
            task_planilha.write(row_num, 7, task.end_date)
            task_planilha.write(row_num, 10, task.op_cwp)
            task_planilha.write(row_num, 11, task.OP_PACOTE_DE_SUPRIMENTOS)

            try:
                task_planilha.write(row_num, 5, valores[0], formato_percentual)
                dict_avanco[task.activity_id] = valores[0]
            except:
                task_planilha.write(row_num, 5, None, formato_percentual)
                dict_avanco[task.activity_id] = 0
            try:
                task_planilha.write(row_num, 8, valores[1], formato_data)
            except:
                task_planilha.write(row_num, 8, None)
            try:
                task_planilha.write(row_num, 9, valores[2], formato_data)
            except:
                task_planilha.write(row_num, 9, None)


            row_num += 1

    task_planilha.set_column('A:A', 21.86)
    task_planilha.set_column('B:B', 13.00)
    task_planilha.set_column('C:C', 20.14)
    task_planilha.set_column('D:D', 119.00)
    task_planilha.set_column('E:E', 18.29)
    task_planilha.set_column('F:F', 21.57)
    task_planilha.set_column('G:G', 17.43)
    task_planilha.set_column('H:H', 17.43)
    task_planilha.set_column('I:I', 17.43)
    task_planilha.set_column('J:J', 17.43)
    task_planilha.set_column('K:K', 28.71)
    task_planilha.set_column('L:L', 43.71)
    task_planilha.set_column('M:M', 18.14)


def planilha_taskrsrc(taskrsrc_planilha, recursos, avancos, wb, dict_avanco):


    taskrsrc_planilha.write_row(0, 0, ['rsrc_id', 'task_id', 'TASK__status_code', 'role_id', 'acct_id','rsrc_type', 'act_start_date', 'act_end_date','target_qty', 'act_qty', 'remain_qty','target_cost','remain_qty','target_cost', 'act_cost','remain_cost', 'delete_record_flag'])
    taskrsrc_planilha.write_row(1, 0, ['Resource ID', 'Activity ID', '(*)Activity Status', 'Role ID', 'Cost Account ID', '(*)Resource Type','Actual Start','Actual Finish', 'Budgeted Units(h)', 'Actual Units(h)', 'Remaining Early Units(h)', 'Budgeted Cost', 'Actual Cost','Remaining Cost', 'Delete This Row'])

    row_num = 2

    for recurso in recursos:
        if recurso.activity_id in dict_avanco.keys():
            taskrsrc_planilha.write(row_num, 0, recurso.rsrc_id)
            taskrsrc_planilha.write(row_num, 1, recurso.activity_id)
            taskrsrc_planilha.write(row_num, 2, recurso.task_status_code)
            taskrsrc_planilha.write(row_num, 3, recurso.role_id)
            taskrsrc_planilha.write(row_num, 4, recurso.acct_id)
            taskrsrc_planilha.write(row_num, 5, recurso.rsrc_type)
            taskrsrc_planilha.write(row_num, 6, recurso.act_start_date)
            taskrsrc_planilha.write(row_num, 7, recurso.act_end_date)
            taskrsrc_planilha.write(row_num, 8, recurso.target_qty)
            taskrsrc_planilha.write(row_num, 11, recurso.target_cost)
            try:
                taskrsrc_planilha.write(row_num, 9, dict_avanco[recurso.activity_id] * recurso.target_qty)
                taskrsrc_planilha.write(row_num, 10, recurso.target_qty - (dict_avanco[recurso.activity_id] * recurso.target_qty))

                taskrsrc_planilha.write(row_num, 12, dict_avanco[recurso.activity_id] * recurso.target_cost)
                taskrsrc_planilha.write(row_num, 13,recurso.target_cost - (dict_avanco[recurso.activity_id] * recurso.target_cost))
            except:
                pass

            row_num += 1

    taskrsrc_planilha.set_column('A:A', 27.71)
    taskrsrc_planilha.set_column('B:B', 17.71)
    taskrsrc_planilha.set_column('C:C', 20.57)
    taskrsrc_planilha.set_column('D:D', 19.29)
    taskrsrc_planilha.set_column('E:E', 19.29)
    taskrsrc_planilha.set_column('F:F', 19.29)
    taskrsrc_planilha.set_column('G:G', 16.00)
    taskrsrc_planilha.set_column('H:H', 16.00)
    taskrsrc_planilha.set_column('I:I', 16.71)
    taskrsrc_planilha.set_column('J:J', 14.00)
    taskrsrc_planilha.set_column('K:K', 22.43)
    taskrsrc_planilha.set_column('L:L',  13.29)
    taskrsrc_planilha.set_column('M:M', 10.14)
    taskrsrc_planilha.set_column('N:N', 14.14)
    taskrsrc_planilha.set_column('O:O', 17.43)



def planilha_userdata(userdata, wb):

    userdata.write_row(0, 0, ['user_data'])
    userdata.write_row(1, 0, ['UserSettings Do Not Edit'])
    userdata.write_row(2, 0, ['DurationQtyType=QT_Day ShowAsPercentage=0 SmallScaleQtyType=QT_Hour'])


