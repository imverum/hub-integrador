import xlsxwriter as xls

def valida_op(id, op, ops_master):
    valida = op in ops_master
    if valida:
        return None
    else:
        return [id, op, "Op não encontra no cronograma master"]


def valida_qtdavanco_maior_qtdplanejado(id, qtdavanco, qtdplanejado):
    try:
        valida = qtdavanco > qtdplanejado
    except:
        valida = False

    if valida:
        return [id, f'valor Real: {qtdavanco} / valor Planejado: {qtdplanejado}', "Quantidade real maior do que o planejado"]
    else:
        return None



def cria_planilha_validacao(output, ops_master, atividades):
    wb = xls.Workbook(output)

    planilhas_logs = wb.add_worksheet("Logs")

    planilha(planilhas_logs, ops_master, atividades, wb)

    wb.close()


def planilha(planilhas_logs, ops_master, atividades, wb):
    planilhas_logs.write_row(0, 0, ['ID', 'Dado', 'Erro'])

    row_num = 1

    for atividade in atividades:
        validacao = valida_op(atividade.id, atividade.OP_WP, ops_master)
        if validacao:
            planilhas_logs.write(row_num, 0, validacao[0])
            planilhas_logs.write(row_num, 1, validacao[1])
            planilhas_logs.write(row_num, 2, validacao[2])

            row_num += 1

        validarealmaiorplanejado = valida_qtdavanco_maior_qtdplanejado(atividade.id, atividade.actual, atividade.previsto)
        if validarealmaiorplanejado:
            planilhas_logs.write(row_num, 0, validarealmaiorplanejado[0])
            planilhas_logs.write(row_num, 1, validarealmaiorplanejado[1])
            planilhas_logs.write(row_num, 2, validarealmaiorplanejado[2])

            row_num += 1

