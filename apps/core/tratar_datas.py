import datetime

data_2_str = "10/02/2023 10:09"
data_2 = datetime.datetime.strptime(data_2_str, "%d/%m/%Y %H:%M")

if isinstance(data_2, datetime.datetime):
    print("A variável contém informações de data e hora.")
else:
    print("A variável contém apenas informações de data.")

def tratar_data(data):
    try:
        data_variavel = datetime.datetime.strptime(data, "%d/%m/%Y %H:%M")
        return data_variavel
    except:
        pass

    try:
        data_variavel = datetime.datetime.strptime(data, "%d/%m/%Y")
        return data_variavel
    except:
        pass

