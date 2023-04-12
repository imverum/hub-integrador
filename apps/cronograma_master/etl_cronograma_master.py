from apps.core.tratar_datas import tratar_data, validar_data
from apps.cronograma_master.models import ConfiguraCronogramaMaster, LogProcessamentoCronogramaMaster, \
    StageCronogramaMaster, ADFCronoMaster
from apps.projeto.models import Projeto
import pandas as pd
from datetime import datetime

def run_crono_master (arquivold_file, projeto_id, crono, request):
    projeto = Projeto.objects.get(id=projeto_id)
    configuracoes = ConfiguraCronogramaMaster.objects.filter(projeto=projeto).values().first()

    sheet_names = pd.ExcelFile(arquivold_file)
    if not configuracoes["planilha"] in sheet_names.sheet_names:
        log = LogProcessamentoCronogramaMaster.objects.create(
            projeto=crono.projeto,
            tipo="CRONO_MASTER_PROCESSAMENTO",
            log="Planilha " + configuracoes["planilha"] + " não foi encontrada",
            execucao=crono,

        )
        crono.status = 'ERRO'
        crono.save()

    if crono.status != "ERRO":
        ################################leitura do excel

        df_crono = pd.read_excel(arquivold_file, sheet_name=configuracoes["planilha"],
                              skiprows=int(configuracoes["linha"]))

        ################################remove colunas em branco

        df_crono = df_crono.drop(columns=df_crono.columns[0:int(configuracoes["coluna"])])


        ################################validando colunas
        valida_colunadf(df_crono, crono, request, configuracoes)
        if crono.status != "ERRO":

            colunas_obrigatorias = [configuracoes["activity_id"], configuracoes["resource_name"], configuracoes["resource_type"], configuracoes["spreadsheet_field"]]

            colunas_datas = [coluna for coluna in df_crono.columns if validar_data(coluna)]

            todas_colunas = colunas_obrigatorias + colunas_datas

            colunas_extras = set(df_crono.columns) - set(todas_colunas)
            if len(colunas_extras) > 0:
                df_crono = df_crono.drop(columns=list(colunas_extras))

            colunas_datas_tratadas = []
            for coluna in df_crono.columns:
                if coluna not in colunas_obrigatorias:
                    try:
                        data_str = coluna.strftime("%d/%m/%Y %H:%M:%S")
                        colunas_datas_tratadas.append(data_str)

                    except:
                        colunas_datas_tratadas.append(coluna)

            colunas_tratadas = colunas_obrigatorias + colunas_datas_tratadas

            df_crono.columns = colunas_tratadas

            df_crono = df_crono.melt(id_vars=[ configuracoes["activity_id"], configuracoes["resource_name"], configuracoes["resource_type"], configuracoes["spreadsheet_field"]],
                                      var_name='Data', value_name='Valor')


            df_crono = df_crono.dropna(subset=['Valor'])

            valor_unidade = df_crono['Valor'].str.extract('(\d+)\s*([a-zA-Z]+)')

            df_crono['Valor'] = valor_unidade[0]

            df_crono['Valor'] = pd.to_numeric(df_crono['Valor'])

            df_crono['Unidade'] = valor_unidade[1]

            df_crono['Data'] = df_crono['Data'].str.replace('-', '/')

            for dado in range(len(df_crono)):
                try:
                    activity_id = df_crono[configuracoes["activity_id"]].iloc[dado]
                    if pd.isna(activity_id):
                        activity_id = None
                except:
                   pass
                try:
                    resource_name = df_crono[configuracoes["resource_name"]].iloc[dado]
                    if pd.isna(resource_name):
                        resource_name = None
                except:
                   pass

                try:
                    resource_type = df_crono[configuracoes["resource_type"]].iloc[dado]
                    if pd.isna(resource_type):
                        resource_type = None
                except:
                    pass

                try:
                    spreadsheet_field = df_crono[configuracoes["spreadsheet_field"]].iloc[dado]
                    if pd.isna(spreadsheet_field):
                        spreadsheet_field = None
                except:
                    pass
                try:
                    data = df_crono["Data"].iloc[dado]
                    print(data)
                    data = tratar_data(df_crono["Data"].iloc[dado])
                    print(data)
                    if pd.isna(data):
                        data = None
                except:
                    pass

                try:
                    valor = df_crono["Valor"].iloc[dado]
                    if pd.isna(valor):
                        valor = None
                except:
                    pass

                try:
                    unidade = df_crono["Unidade"].iloc[dado]
                    if pd.isna(unidade):
                        unidade = None
                except:
                    pass

                carga_stage = StageCronogramaMaster.objects.create(
                    execucao=crono,
                    projeto=crono.projeto,
                    activity_id=activity_id,
                    resource_name=resource_name,
                    resource_type=resource_type,
                    spreadsheet_field=spreadsheet_field,
                    data= data, #datetime.strptime(str(data), "%Y-%m-%d %H:%M:%S")
                    valor=valor,
                    unidade=unidade,
                )
            carga_adf_crono_master = ADFCronoMaster.objects.create(
                execucao=crono,
            )


def valida_colunadf(df_crono, crono, request, configuracoes):
    colunas_errors = []
    if not configuracoes["activity_id"] in df_crono.columns:

        colunas_errors.append("A Coluna " + configuracoes["activity_id"] + " não foi encontrada")

    if not configuracoes["resource_name"] in df_crono.columns:

        colunas_errors.append("A Coluna " + configuracoes["resource_name"] + " não foi encontrada")

    if not configuracoes["resource_type"] in df_crono.columns:

        colunas_errors.append("A Coluna " + configuracoes["resource_type"] + " não foi encontrada")

    if not configuracoes["spreadsheet_field"] in df_crono.columns:

        colunas_errors.append("A Coluna " + configuracoes["spreadsheet_field"] + " não foi encontrada")


    if len(colunas_errors) > 0:
        for erro in colunas_errors:

            log = LogProcessamentoCronogramaMaster.objects.create(
                projeto=crono.projeto,
                tipo="CRONO_MASTER_PROCESSAMENTO",
                log=erro,
                execucao=crono,

            )
        crono.status = 'ERRO'
        crono.save()

    else:
        pass


