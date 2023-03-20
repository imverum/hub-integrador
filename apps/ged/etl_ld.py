import pandas as pd





def gerar_cronograma(nova_planilha, output):

    run_awp(nova_planilha, output)



def run_ld(arquivold_file):
    ################################leitura do excel
    df_ld = pd.read_excel(arquivold_file, 'ld')
    print(df_ld)


    ################################lod



    ################################tratamento



    ################################carga_stage_ld



