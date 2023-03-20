from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from apps.account.forms import LoginForm, UserRegistrationForm, RegisterFormset, UserEditFormAdmin, \
    UserProfileEditFormAdmin, EditAdminFormset
from apps.core.models import Owner
from apps.usuario.models import Profile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'], password=cd['password'])
        else:render(request, 'registration/login.html', {'form':form})


        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')

    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form':form})



@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'], password=cd['password'])

        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')

    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form':form})


@csrf_exempt
@login_required
def register(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    qtd_usuarios = Profile.objects.filter(owner=profile.owner).count()
    owner = Owner.objects.get(owner=profile.owner)
    #if qtd_usuarios >= owner.qtd_user:
    #    messages.error(request, 'Quantidade máxima de Usuarios cadastrada atingida, entre em contato com a administração do sistema!')
    #    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        user_instance = User()
        user_form = UserRegistrationForm(request.POST or None,instance=user_instance)
        user_profile_formset = RegisterFormset(request.POST or None, instance=user_instance)



        if user_form.is_valid() and user_profile_formset.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.username = new_user.email

            try:
                new_user.save()
                user_profile_formset.save()
                Profile.objects.filter(user=new_user).update(owner=owner)

            except:
                user_form = UserRegistrationForm(request.POST or None)
                user_profile_formset = RegisterFormset(request.POST or None)
                messages.error(request, 'Usuário já cadastrado com esse e-mail')

                return render(request, 'registration/register.html',
                          {'user_form': user_form, 'user_profile_formset': user_profile_formset})
            return redirect('list_user')
        else:
            user_form = UserRegistrationForm(request.POST or None)
            user_profile_formset = RegisterFormset(request.POST or None)

            return render(request, 'registration/register.html',
                          {'user_form': user_form, 'user_profile_formset': user_profile_formset})

    else:
        user_instance = User()
        user_form = UserRegistrationForm(request.POST or None, instance=user_instance)
        user_profile_formset = RegisterFormset(request.POST or None, instance=user_instance)

        return render(request, 'registration/register.html',
                          {'user_form': user_form, 'user_profile_formset': user_profile_formset})

@csrf_exempt
@login_required
def usuario_deletar(request):
    usuario_id = request.POST.get("id_delet")
    usuario = User.objects.get(id=usuario_id)
    usuario.delete()
    messages.success(request, "Usuário excluido com sucesso !")
    return redirect('list_user')

@csrf_exempt
@login_required
def usuario_edit_admin(request):
    usuario_id = request.POST.get("id_edit")
    if request.method == 'POST':
        profile_instance = Profile.objects.get(id=usuario_id)
        user_instance = User.objects.get(id=profile_instance.user.id)
        form_edit_user_admin = UserEditFormAdmin(request.POST or None, instance=user_instance)
        user_profile_edit = UserProfileEditFormAdmin(request.POST or None, instance=profile_instance)
        if user_profile_edit.is_valid() and form_edit_user_admin.is_valid():
            form_edit_user_admin.save()
            user_profile_edit.save()
            return redirect('list_user')
        else:
            return redirect('list_user')
@csrf_exempt
@login_required
def usuario_edit_admin_ajax(request, pk):
    usuario = User.objects.get(id=pk)
    profile = Profile.objects.get(user=usuario)

    data = {
        'is_active': usuario.is_active,
        'role': profile.role,
    }

    return JsonResponse(data)