from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.fornecedores.forms import FornecedorRegisterForm
from apps.fornecedores.models import Fornecedores

from apps.usuario.models import Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse

@csrf_exempt
@login_required
def list_fornecedores(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    fornecedores = Fornecedores.objects.filter(owner=profile.owner)
    fornecedor_form = FornecedorRegisterForm(request.POST or None)


    return render(request, 'list_fornecedores.html',
                  {'fornecedores': fornecedores, 'fornecedor_form': fornecedor_form, 'profile': profile})

@csrf_exempt
@login_required
def adicionar_fornecedor(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    fornecedor_instance = Fornecedores()
    fornecedor_form = FornecedorRegisterForm(request.POST or None, instance=fornecedor_instance)

    if request.method == "POST":
        if fornecedor_form.is_valid():
            fornecedor_novo = request.POST.get('fornecedor')
            count = Fornecedores.objects.filter(fornecedor=fornecedor_novo, owner=profile.owner).count()
            if count > 0:
                messages.error(request, 'Fornecedor já cadastrada!!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            fornecedor = fornecedor_form.save(commit=False)
            fornecedor.owner = profile.owner
            fornecedor.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def fornecedor_edit_ajax(request, pk):
    fornecedor = Fornecedores.objects.get(id=pk)

    data = {
        'fornecedor': fornecedor.fornecedor,
        'cnpj': fornecedor.cnpj,
        'pais': fornecedor.pais,
        'estado': fornecedor.estado,
        'bairro': fornecedor.bairro,
        'rua': fornecedor.rua,
        'cep': fornecedor.cep,
        'descricao': fornecedor.descricao,
    }

    return JsonResponse(data)




@login_required
def fornecedor_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    id = request.POST.get("id_edit")
    fornecedor_instance = Fornecedores.objects.get(id=id)
    fornecedor_form = FornecedorRegisterForm(request.POST or None, instance=fornecedor_instance)
    if request.method == "POST":

        if fornecedor_form.is_valid():
            fornecedor_edit = request.POST.get('fornecedor_edit')
            count = Fornecedores.objects.filter(fornecedor=fornecedor_edit, owner=profile.owner).count()
            if count > 0:
                messages.error(request, 'Fornecedor já cadastrada!!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            fluxo = fornecedor_form.save(commit=False)
            try:
                fluxo.save()
            except:
                # messages.error(request, 'Usuário já cadastrado com esse e-mail')

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
@login_required
def fornecedor_deletar(request):
    id = request.POST.get('id_delet')
    fornecedor = Fornecedores.objects.get(id=id)
    fornecedor.delete()
    messages.success(request, "Fornecedor deletado com sucesso!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

