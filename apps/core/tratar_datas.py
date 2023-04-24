from datetime import datetime



def tratar_data(data):
    try:
        print(data)
        data_variavel = datetime.strptime(data, "%d/%m/%Y %H:%M")
        return data_variavel
    except:
        pass

    try:
        data_variavel = datetime.strptime(data, "%DD/%MM/%YYYY")
        return data_variavel

    except:
        pass

    try:
        data_variavel = datetime.strptime(data, "%d/%m/%Y")
        return data_variavel
    except:
        pass
    try:
        data_variavel = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        return data_variavel
    except:
        pass

    try:
        data_variavel = datetime.strptime(data, '%d/%b/%y').strftime('%Y-%m-%d')
        return data_variavel
    except:
        pass

    try:
        data_variavel = datetime.strptime(data, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d')
        return data_variavel
    except:
        pass


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
        data_variavel = datetime.strptime(data, '%d/%b/%y').strftime('%d/%m/%Y')
        return True
    except:
        pass
    try:
        data_variavel = datetime.strptime(data, '%d-%b-%y').strftime('%d-%m-%Y')
        return True
    except:
        return type(data) == datetime
