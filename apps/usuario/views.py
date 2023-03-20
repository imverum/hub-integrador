from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from apps.account.forms import UserEditFormAdmin, UserProfileEditFormAdmin
from apps.core.models import Usuario_Unidade
from apps.projeto.models import Usuario_Projeto
from apps.usuario.forms import UserProfileEditForm, RegisterFormset, UserEditForm, UnidadeAddForm, ProjetoUsuarioAddForm
from apps.usuario.models import Profile, ROLE_CHOICE
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def list_user(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    usuarios = Profile.objects.filter(owner=profile.owner)
    user_form = RegisterFormset()
    choices = ROLE_CHOICE

    form_edit_user_admin = UserEditFormAdmin(request.POST or None)
    user_profile_edit = UserProfileEditFormAdmin(request.POST or None)

    return render(request, 'list_user.html',
                  {'usuarios': usuarios, 'user_form': user_form, 'choices': choices, 'profile': profile, 'form_edit_user_admin':form_edit_user_admin, 'user_profile_edit':user_profile_edit})

@csrf_exempt
@login_required
def profile_detail(request):
    id = request.user.id
    usuario = User.objects.get(id=id)
    profile = Profile.objects.get(user=usuario)
    form = UserProfileEditForm(request.POST or None, instance=profile)

    return render(request, 'profile.html', {'usuario':usuario,'profile':profile, 'form':form})


@csrf_exempt
@login_required
def profile_edit(request, id):
    usuario = User.objects.get(id=id)
    profile = Profile.objects.get(user=usuario)
    form = UserProfileEditForm(request.POST or None, instance=profile)

    if request.method == "POST":

        if form.is_valid():
            user_photo = request.FILES.get('user_photo')
            if user_photo != None:
                profile_user = form.save(commit=False)
                profile_user.user_photo= user_photo
                profile_user.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
@login_required
def profile_detail(request):
    usuario = request.user
    unidades = Usuario_Unidade.objects.filter(usuario_id=usuario)
    projetos = Usuario_Projeto.objects.filter(usuario_id=usuario)
    profile = Profile.objects.get(user=usuario)
    profile_perfil = Profile.objects.get(user=request.user)
    form_profile = UserEditForm(request.POST or None, instance=profile)
    form_unidade = UnidadeAddForm(request.POST or None, instance=usuario)
    form_projeto_usuario = ProjetoUsuarioAddForm(request.POST or None)

    return render(request, 'profile.html', {'projetos':projetos, 'usuario':usuario, 'form_profile':form_profile, 'form_unidade':form_unidade,'unidades':unidades, 'profile':profile, 'profile_perfil':profile_perfil, 'form_projeto_usuario':form_projeto_usuario})


@csrf_exempt
@login_required
def profile_detail_visita(request, id):
    usuario = User.objects.get(id=id)
    unidades = Usuario_Unidade.objects.filter(usuario=usuario)
    form = UserEditForm(request.POST or None, instance=usuario)
    form_unidade = UnidadeAddForm(request.POST or None, instance=usuario)

    return render(request, 'profile.html', {'usuario':usuario, 'form':form, 'form_unidade':form_unidade,'unidades':unidades})

@csrf_exempt
@login_required
def profile_edit(request, id):
    usuario = User.objects.get(id=id)
    profile = Profile.objects.get(user=usuario)
    form_profile = UserEditForm(request.POST or None, instance=profile)

    if request.method == "POST":
        if form_profile.is_valid():
            form_profile.save()
            user_photo = request.FILES.get('user_photo')
            if user_photo != None:
                profile_user = form_profile.save(commit=False)
                Profile.objects.filter(id=profile_user.id).update(user_photo=user_photo)
                profile_user.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                form_profile.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required
def adicionar_unidade(request, id):
    usuario = User.objects.get(id=id)
    unidade_instance = Usuario_Unidade()
    form_unidade = UnidadeAddForm(request.POST or None, instance=unidade_instance)
    print(form_unidade.is_valid())

    if request.method == "POST":
        if form_unidade.is_valid():
            unidade_nova = request.POST.get('unidade')
            count = Usuario_Unidade.objects.filter(unidade=unidade_nova, usuario=usuario).count()
            if count > 0:
                messages.error(request, 'Unidade já cadastrada para o usuario!!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            unidade = form_unidade.save(commit=False)
            unidade.usuario = usuario
            unidade.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
@login_required
def deletar_unidade(request, id):
    unidade = Usuario_Unidade.objects.get(id=id)
    unidade.delete()
    messages.success(request, "Disciplina Excluida com sucesso !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required
def adicionar_projeto(request, id):
    usuario = User.objects.get(id=id)
    projeto_instance = Usuario_Projeto()
    form_projeto_usuario = ProjetoUsuarioAddForm(request.POST or None, instance=projeto_instance)

    if request.method == "POST":
        if form_projeto_usuario.is_valid():
            projeto_novo = request.POST.get('projeto')
            count = Usuario_Projeto.objects.filter(projeto=projeto_novo, usuario=usuario).count()
            if count > 0:
                messages.error(request, 'Projeto já cadastrada para o usuario!!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            projeto = form_projeto_usuario.save(commit=False)
            projeto.usuario = usuario
            projeto.unidade = projeto.projeto.unidade
            projeto.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
@login_required
def deletar_projeto(request, id):
    projeto = Usuario_Projeto.objects.get(id=id)
    projeto.delete()
    messages.success(request, "Projeto Excluido com sucesso !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))