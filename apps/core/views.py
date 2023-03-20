from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from apps.usuario.models import Profile


@login_required
def home(request):
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    contexto = {'profile':profile}
    return render(request, 'index.html', contexto)
