from datetime import datetime
import pandas as pd


def tratar_data(data):
    if pd.isna(data):
        data_variavel = None
        print("AQUIIII")
        return data_variavel
    try:
        print(data)
        print("1")
        data_variavel = datetime.strptime(data.strip(), "%d/%m/%Y %H:%M").date()
        return data_variavel
    except:
        pass

    try:
        print("2")
        data_variavel = datetime.strptime(data.strip(), "%DD/%MM/%YYYY").date()
        return data_variavel

    except:
        pass

    try:
        print("3")
        data_variavel = datetime.strptime(data.strip(), "%d/%m/%Y").date()
        return data_variavel
    except:
        pass
    try:
        print("4")
        data_variavel = datetime.strptime(data.strip(), "%Y-%m-%d %H:%M:%S").date()
        return data_variavel
    except:
        pass
    try:
        print("5")
        data_variavel = datetime.strptime(data.strip(), "%Y-%m-%d").date()
        return data_variavel
    except:
        pass
    try:
        data_variavel = datetime.strptime(data.strip(), "%Y/%m/%d").date()
        return data_variavel
    except:
        pass

    try:
        print("6")
        data_variavel = datetime.strptime(data.strip(), '%d/%b/%y').strftime('%Y-%m-%d').date()
        return data_variavel
    except:
        pass

    try:
        print("7")
        data_variavel = datetime.strptime(data.strip(), '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d').date()
        return data_variavel
    except:
        print("8")
        pass
    try:
        print("9")

        data_variavel = datetime.strptime(data.strip(), "%Y-%m-%d").date()
        return data_variavel
    except ValueError:

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
