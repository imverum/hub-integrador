from django.db import models

from apps.core.models import Owner, Unidade
from apps.projeto.models import Projeto
from apps.usuario.models import Profile


class ExecucaoLD(models.Model):
    arquivold = models.FileField(upload_to='media/', null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, blank=True, null=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT, blank=True, null=True)
    data_corte = models.DateField(blank=True, null=True)
    data_execucao = models.DateField(auto_now=True, blank=True, null=True)
    inicio = models.DateTimeField(blank=True, null=True)
    termino = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length= 200, blank=True, null=True)
    tipo = models.CharField(max_length= 200, blank=True, null=True)


    class Meta:
        db_table = 'dbo_execucao_ld'
        verbose_name_plural = 'BD Execucao LD'
        verbose_name = 'BD Execucao LD'

class StageLd(models.Model):
    execucao = models.ForeignKey(ExecucaoLD, on_delete=models.PROTECT, blank=True, null=True)
    sk = models.IntegerField(blank=True, null=True)
    documento = models.CharField(max_length= 200, blank=True, null=True)
    numero_contratada = models.CharField(max_length= 200, blank=True, null=True)
    empresa = models.CharField(max_length= 200, blank=True, null=True)
    tipo_emissao_inicial = models.CharField(max_length= 200, blank=True, null=True)
    certifica_na_1a_emissao = models.BooleanField(blank=True, null=True)
    data_emissão_inicial_prevista = models.DateField(blank=True, null=True)
    data_emissão_inicial_reprogramada = models.DateField(blank=True, null=True)
    status_ld = models.CharField(max_length= 200, blank=True, null=True)
    titulo = models.CharField(max_length= 200,blank=True, null=True)
    tipo_documento = models.CharField(max_length= 200, blank=True, null=True)
    formato = models.CharField(max_length= 200, blank=True, null=True)
    paginas = models.IntegerField(blank=True, null=True)
    a1_equivalente = models.DecimalField(max_digits= 200,decimal_places=2,  blank=True, null=True)
    codigo_atividade = models.CharField(max_length= 200, blank=True, null=True)
    work_package_area = models.CharField(max_length= 200,blank=True, null=True)
    work_package = models.CharField(max_length= 200, blank=True, null=True)


    class Meta:
        db_table = 'db_stage_ld'
        verbose_name_plural = 'BD Stage LD'
        verbose_name = 'BD Stage LD'

class ConfiguraLd(models.Model):
        owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
        unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, blank=True, null=True)
        projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT, blank=True, null=True)
        documento = models.CharField(max_length=200, blank=True, null=True)
        numero_contratada = models.CharField(max_length=200, blank=True, null=True)
        titulo = models.CharField(max_length=200, blank=True, null=True)
        status_ld = models.CharField(max_length=200, blank=True, null=True)
        codigo_atividade = models.CharField(max_length=200, blank=True, null=True)
        sk = models.CharField(max_length=200, blank=True, null=True)
        data_emissão_inicial_prevista = models.CharField(max_length=200, blank=True, null=True)
        paginas = models.CharField(max_length=200, blank=True, null=True)
        a1_equivalente = models.CharField(max_length=200, blank=True, null=True)

        class Meta:
            db_table = 'db_configura_ld'
            verbose_name_plural = 'BD Configura LD'
            verbose_name = 'BD Configura LD'
