import io
import os
from django.contrib import messages
from azure.storage.blob import BlobServiceClient
from django.http import HttpResponse, HttpResponseRedirect
from decouple import config

from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta



# obtenha a instância BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=verumsys;AccountKey=zsjENq7RHecRcbSOGJrIjaXdV/z4kh0KtTsf/J/xy1FeANFcnXSnh6LDytspbpbF4Q5OwJOK4UnC+ASt4uembg==;EndpointSuffix=core.windows.net")

def conector_blob(ld, arquivo_file):
    # gere um nome de blob exclusivo usando um UUID aleatório
    nome_original, extensao = os.path.splitext(arquivo_file.name)
    blob_name = nome_original + '_' + str(ld.id) + extensao


    # obtenha uma referência para o contêiner Blob que você deseja usar
    container_client = blob_service_client.get_container_client("interfacehubintegrador")


    # crie um blob no contêiner Blob
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(arquivo_file)

    return blob_name


def download_file(request, file_name):
    try:

        container_client = blob_service_client.get_container_client("interfacehubintegrador")
        # Obtenha uma referência ao blob
        blob_client = container_client.get_blob_client(file_name)

        # Obtenha o conteúdo do blob
        content = blob_client.download_blob().readall()

        # Crie uma resposta HTTP com o conteúdo do arquivo
        response = HttpResponse(content, content_type='application/octet-stream')

        # Defina o nome do arquivo como o nome original do arquivo
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return response
    except:
        messages.error(request, 'Arquivo não encontrado!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def arquiv_xer_storage(blob_name):

    blob_client = blob_service_client.get_blob_client(container="interfacehubintegrador", blob=blob_name)

    # Download do arquivo XER do Azure Blob Storage
    #blob_data = blob_client.download_blob()
    #xer_content = blob_data.content_as_bytes()
    #blob_url = blob_client.url

    #blob_url = blob_service_client.make_blob_url("interfacehubintegrador", blob_name)


    #file_path = blob_url.split("verumsys" + '.blob.core.windows.net/')[1]


    #file_bytes = blob_client.download_blob(max_concurrency=1).readall()
    #blob_data = blob_client.download_blob().content_as_bytes()

    blob_url = blob_client.url
    print(blob_url)
    print("blob")
    print(blob_url)
    print("blob")
    print(blob_url)
    # Passa o objeto de fluxo de bytes para a função de processamento do arquivo
    return blob_url



def caminho_file(request, file_name):
    try:
        account_name = 'verumsys'
        account_key = 'zsjENq7RHecRcbSOGJrIjaXdV/z4kh0KtTsf/J/xy1FeANFcnXSnh6LDytspbpbF4Q5OwJOK4UnC+ASt4uembg=='
        container_name = 'interfacehubintegrador'

        # Crie o serviço do blob
        blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net",
                                                credential=account_key)

        # Obtenha a referência para o blob
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(file_name)

        # Gere uma URL de Assinatura Compartilhada (SAS) para o blob
        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            blob_name=file_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1),  # Defina o tempo de expiração apropriado
        )

        blob_url_with_sas = f"{blob_client.url}?{sas_token}"
        print("blob_url_with_sas")
        print(blob_url_with_sas)

        return blob_url_with_sas



    except:
        messages.error(request, 'Arquivo não encontrado!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



