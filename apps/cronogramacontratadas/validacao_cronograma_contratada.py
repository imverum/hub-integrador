import xlsxwriter as xls

def valida_op(id, op, ops_master):
    valida = op in ops_master
    if not op == None:
        if op.endswith("000"):
            return None
        if valida:
            return None
        else:
            return [id, op, "Op não encontra no cronograma master"]
    return None


def valida_qtdavanco_maior_qtdplanejado(id, qtdavanco, qtdplanejado):
    try:
        valida = qtdavanco > qtdplanejado
    except:
        valida = False

    if valida:
        return [id, f'valor Real: {qtdavanco} / valor Planejado: {qtdplanejado}', "Quantidade real maior do que o planejado"]
    else:
        return None


def valida_ponderacao(id, qtdplanejado, OP_WP):
    print("qtdplanejado")
    print(type(qtdplanejado))
    if not OP_WP == None:
        if OP_WP.endswith("000"):
            return None

        if qtdplanejado == 0 or qtdplanejado == None or qtdplanejado == "0":
            return [id, qtdplanejado,f'Não foi encontrado valor trabalho planejado na atividade']
    return None

def valida_atraso_dias_atividade(id, avanco, data_fim_bl, data_fim_reprogramado):
    if avanco >= 100 or data_fim_reprogramado is None or data_fim_bl is None:
        return None

    elif data_fim_reprogramado > data_fim_bl:
        atraso = data_fim_bl-data_fim_reprogramado
        if atraso.days > 1:
            valor = "dias"
        else:
            valor = "dia"
        return [id, f"data fim bl:{data_fim_bl} - data fim prevista{data_fim_reprogramado}",f'A Atividade apresenta um atraso de {atraso.days} {valor}']

def cria_planilha_validacao(output, ops_master, atividades):
    wb = xls.Workbook(output)

    planilhas_logs = wb.add_worksheet("Logs")

    planilha(planilhas_logs, ops_master, atividades, wb)

    wb.close()


def planilha(planilhas_logs, ops_master, atividades, wb):
    planilhas_logs.write_row(0, 0, ['ID', 'Dado', 'Erro'])

    row_num = 1

    for atividade in atividades:
        validacao = valida_op(atividade.activity_id, atividade.OP_WP, ops_master)
        if validacao:
            planilhas_logs.write(row_num, 0, validacao[0])
            planilhas_logs.write(row_num, 1, validacao[1])
            planilhas_logs.write(row_num, 2, validacao[2])

            row_num += 1

        validarealmaiorplanejado = valida_qtdavanco_maior_qtdplanejado(atividade.activity_id, atividade.actual, atividade.previsto)
        if validarealmaiorplanejado:
            planilhas_logs.write(row_num, 0, validarealmaiorplanejado[0])
            planilhas_logs.write(row_num, 1, validarealmaiorplanejado[1])
            planilhas_logs.write(row_num, 2, validarealmaiorplanejado[2])

            row_num += 1
        validaponderacao = valida_ponderacao(atividade.activity_id, atividade.previsto, atividade.OP_WP)
        if validaponderacao:
            planilhas_logs.write(row_num, 0, validaponderacao[0])
            planilhas_logs.write(row_num, 1, validaponderacao[1])
            planilhas_logs.write(row_num, 2, validaponderacao[2])

            row_num += 1

        validaatrasodiasatividade = valida_atraso_dias_atividade(atividade.activity_id, atividade.avanco, atividade.data_fim_bl, atividade.data_fim_reprogramado)
        if validaatrasodiasatividade:
            planilhas_logs.write(row_num, 0, validaatrasodiasatividade[0])
            planilhas_logs.write(row_num, 1, validaatrasodiasatividade[1])
            planilhas_logs.write(row_num, 2, validaatrasodiasatividade[2])

            row_num += 1
