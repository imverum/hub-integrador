from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from apps.usuario.models import Profile

@csrf_exempt
@login_required
def home(request):
    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    contexto = {'profile':profile}
    return render(request, 'index.html', contexto)
