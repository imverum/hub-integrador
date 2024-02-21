from datetime import datetime
import pandas as pd


def tratar_data(data):
    if pd.isna(data):
        print("AQUIIII")
        return None

    formatos = [
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%b/%y",
        "%d-%m-%Y %H:%M:%S",
        "%d-%m-%Y",
        '%d/%m/%Y %H:%M:%S',
        '%d-%m-%Y %H:%M:%S',
        "%Y/%m/%d %H:%M:%S",
        "%DD/%MM/%YYYY",
        '%d/%b/%y',
    ]

    for formato in formatos:
        try:
            data_variavel = datetime.strptime(data.strip(), formato)
            return data_variavel.date()
        except ValueError:
            pass

    print(f"Erro ao tratar a data {data}")
    return None


def validar_data(data):
    try:
        data_variavel = datetime.strptime(data, "%d/%m/%Y %H:%M")
        return True
    except:
        pass

    try:
        data_variavel = datetime.strptime(data, "%d/%m/%Y")
        return True
    except:
        pass
    try:
        data_variavel = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        return True
    except:
        pass
    try:
        data_variavel = datetime.strptime(data, "%Y-%m-%d")
        return True
    except:
        pass

    try:
        data_variavel = datetime.strptime(data, '%d/%b/%y').strftime('%d/%m/%Y')
        return True
    except:
        pass
    try:
        data_variavel = datetime.strptime(data, '%d-%b-%y').strftime('%d-%m-%Y')
        return True
    except:
        return type(data) == datetime
