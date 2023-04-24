from apps.ged.models import lod_processamento, ExecucaoLD, ADFLD
import xlsxwriter as xls
import xlsxwriter.utility as xl_util

def criar_planilha_log_geral(output, logs):
    pass

    wb = xls.Workbook(output)

    log = wb.add_worksheet("log")  # LOGS


    planilha_logs(log, wb, logs)


    wb.close()


def planilha_logs(log, wb, logs):

    log.add_table(xl_util.xl_range_abs(0, 0, logs.count(), 1),
                      {'name': 'wp_type7', 'style': None, 'columns': [{'header': 'Tipo'},
                                                                      {'header': 'Log'},
                                                                      ]})

    log.write_row(0, 0, ['Tipo', 'Log'],
                      wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '11'}))

    row_num = 1

    for dado in logs:
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