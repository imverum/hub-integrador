from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from apps.controlecompras.forms import BOMContratadaFormCarga
from apps.controlecompras.models import ControleBOMCompras
from apps.projeto.models import Projeto
from apps.usuario.models import Profile


@csrf_exempt
@login_required
def list_cargas_bom_compras(request, id):
    projeto = Projeto.objects.get(id=id)

    usuario = request.user
    profile = Profile.objects.get(user=usuario)

    form = BOMContratadaFormCarga(request.POST or None)

    boms = ControleBOMCompras.objects.filter(projeto=projeto)
    contexto = {'projeto':projeto,'usuario':usuario, 'profile':profile, 'boms':boms, "form":form}

    return render(request, 'controlecompras_bom_carga.html', contexto)
