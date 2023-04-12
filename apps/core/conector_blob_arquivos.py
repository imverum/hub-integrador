import io
import os
from django.contrib import messages
from azure.storage.blob import BlobServiceClient
from django.http import HttpResponse, HttpResponseRedirect
from decouple import config


# obtenha a instância BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(config('blob_service_client'))



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


























