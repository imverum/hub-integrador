# import win32com.client
# import pandas as pd
# import pythoncom
# import requests
#
# def conector_project(croonograma, coluna):
#     print(croonograma)
#     pjApp = win32com.client.Dispatch('MSPRoject.Application', pythoncom.CoInitialize())
#     pjApp.FileOpen(croonograma)
#
#     pjProj = pjApp.ActiveProject
#
#     pjTaskList = pjProj.Tasks
#
#     dc = {
#         'Texto 1': 'Text1',
#         'Texto 2': 'Text2',
#         'Texto 3': 'Text3',
#         'Texto 4': 'Text4',
#         'Texto 5': 'Text5',
#         'Texto 6': 'Text6',
#         'Texto 7': 'Text7',
#         'Texto 8': 'Text8',
#         'Texto 9': 'Text9',
#         'Texto 10': 'Text10',
#         'Texto 11': 'Text11',
#         'Texto 12': 'Text12',
#         'Texto 13': 'Text13',
#         'Texto 14': 'Text14',
#         'Texto 15': 'Text15'
#     }
#
#     df_carga = pd.DataFrame(
#         columns=['ID', 'Folga Livre', 'Folga Total', 'Duração', 'Avanço', 'Data Início BL', 'Data Fim BL',
#                  'Data Início Reprogramado', 'Data Fim Reprogramado', 'Data Início Real', 'Data Fim Real',
#                  'Work Package', 'previsto', 'actual', 'OP_WP'])
#
#     for atividade in pjTaskList:
#         df_carga.loc[len(df_carga)] = [str(atividade.UniqueID), str(atividade.FreeSlack), str(atividade.TotalSlack),
#                                        str(atividade.Duration), str(atividade.PercentComplete),
#                                        str(atividade.BaselineStart)[:11],
#                                        str(atividade.BaselineFinish)[:11], str(atividade.Start)[:11],
#                                        str(atividade.Finish)[:11], str(atividade.ActualStart)[:11],
#                                        str(atividade.ActualFinish)[:11], 'Work Package', atividade.Work,
#                                        atividade.ActualWork, getattr(atividade, dc[coluna])]
#
#     pjApp.Quit()
#
#     return df_carga
#
#
#
# def conector_project(cronograma, coluna, access_token=None):
#     if access_token is None:
#         # Se o access_token não for fornecido, continue usando a abordagem existente
#         return conector_project_com(cronograma, coluna)
#
#     # Se access_token estiver presente, use a Microsoft Graph API
#     return conector_project_graph_api(cronograma, coluna, access_token)
#
#
# def conector_project_com(cronograma, coluna):
#     print(cronograma)
#     pjApp = win32com.client.Dispatch('MSPRoject.Application', pythoncom.CoInitialize())
#     pjApp.FileOpen(cronograma)
#
#     pjProj = pjApp.ActiveProject
#     pjTaskList = pjProj.Tasks
#
#     dc = {
#         'Texto 1': 'Text1',
#         'Texto 2': 'Text2',
#         'Texto 3': 'Text3',
#         'Texto 4': 'Text4',
#         'Texto 5': 'Text5',
#         'Texto 6': 'Text6',
#         'Texto 7': 'Text7',
#         'Texto 8': 'Text8',
#         'Texto 9': 'Text9',
#         'Texto 10': 'Text10',
#         'Texto 11': 'Text11',
#         'Texto 12': 'Text12',
#         'Texto 13': 'Text13',
#         'Texto 14': 'Text14',
#         'Texto 15': 'Text15'
#     }
#
#     df_carga = pd.DataFrame(
#         columns=['ID', 'Folga Livre', 'Folga Total', 'Duração', 'Avanço', 'Data Início BL', 'Data Fim BL',
#                  'Data Início Reprogramado', 'Data Fim Reprogramado', 'Data Início Real', 'Data Fim Real',
#                  'Work Package', 'previsto', 'actual', 'OP_WP'])
#
#     for atividade in pjTaskList:
#         df_carga.loc[len(df_carga)] = [str(atividade.UniqueID), str(atividade.FreeSlack), str(atividade.TotalSlack),
#                                        str(atividade.Duration), str(atividade.PercentComplete),
#                                        str(atividade.BaselineStart)[:11],
#                                        str(atividade.BaselineFinish)[:11], str(atividade.Start)[:11],
#                                        str(atividade.Finish)[:11], str(atividade.ActualStart)[:11],
#                                        str(atividade.ActualFinish)[:11], 'Work Package', atividade.Work,
#                                        atividade.ActualWork, getattr(atividade, dc[coluna])]
#
#     return df_carga
#
# def conector_project_graph_api(cronograma, coluna, access_token):
#     # Endpoint da Microsoft Graph API para obter tarefas do projeto
#     graph_endpoint = "https://graph.microsoft.com/v1.0/me/tasks"
#
#     # Parâmetros de consulta para filtrar as tarefas
#     params = {
#         "$filter": f"displayName eq '{cronograma}'"
#     }
#
#     # Cabeçalho de autorização
#     headers = {
#         "Authorization": "Bearer " + access_token
#     }
#
#     # Fazendo a chamada à API
#     response = requests.get(graph_endpoint, params=params, headers=headers)
#
#     if response.status_code == 200:
#         data = response.json()
#
#         # Mapeia os dados para o DataFrame
#         df_carga = pd.DataFrame(columns=['ID', 'DisplayName', 'Status'])
#
#         for task in data["value"]:
#             df_carga.loc[len(df_carga)] = [task["id"], task["displayName"], task["status"]]
#
#         return df_carga
#
#     else:
#         print(f"Falha na chamada à API: {response.status_code}, {response.text}")
#         return None
#
#
# import requests
# from requests.auth import HTTPBasicAuth
#
# # Substitua com suas credenciais
# client_id = '6f7f44fb-6e4b-4414-af18-41fb21361c84'
# client_secret = 'seu_segredo_do_cliente'
# tenant_id = 'seu_id_do_inquilino'
#
# # Obtenha um token de acesso
# token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
# token_data = {
#     'grant_type': 'client_credentials',
#     'client_id': client_id,
#     'client_secret': client_secret,
#     'resource': 'https://graph.microsoft.com'
# }
# token_response = requests.post(token_url, data=token_data)
# access_token = token_response.json().get('access_token')
#
# # Faça uma chamada à Microsoft Graph API para listar tarefas
# project_id = 'id_do_projeto'
# tasks_url = f'https://graph.microsoft.com/v1.0/planner/tasks/{project_id}/tasks'
# headers = {
#     'Authorization': f'Bearer {access_token}',
#     'Content-Type': 'application/json'
# }
# tasks_response = requests.get(tasks_url, headers=headers)
# tasks = tasks_response.json()
#
# print(tasks)