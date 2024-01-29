from django.db import models
from django.db import models

from apps.core.models import Owner, Unidade
from apps.fornecedores.models import Fornecedores
from apps.projeto.models import Projeto
from apps.usuario.models import Profile
# Create your models here.

class CronogramaContratada(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    contratada = models.ForeignKey(Fornecedores, on_delete=models.PROTECT, blank=True, null=True)
    data_ciacao = models.DateTimeField(auto_now=True, blank=True, null=True)
    pacote = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'contratada_container_cronogramas'
        verbose_name_plural = 'BD Contratada Container Cronogramas'
        verbose_name = 'BD Container Cronogramas'





class ExecucaoCronoContratadas(models.Model):
    contratada = models.ForeignKey(CronogramaContratada, on_delete=models.CASCADE, blank=True, null=True)
    arquivo = models.FileField(upload_to='media/', null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, blank=True, null=True, related_name="UnidadeContratada")
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    data_execucao = models.DateTimeField(auto_now=True, blank=True, null=True)
    inicio_preprocessament = models.TimeField(blank=True, null=True)
    termino_preprocessament = models.TimeField(blank=True, null=True)
    inicio_carga = models.TimeField(blank=True, null=True)
    termino_carga = models.TimeField(blank=True, null=True)
    inicio = models.TimeField(blank=True, null=True)
    termino = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length= 200, blank=True, null=True)
    data_corte = models.DateField(blank=True, null=True)


    class Meta:
        db_table = 'contratada_cronograma_contratada'
        verbose_name_plural = 'BD Execucao Cronograma Contratada'
        verbose_name = 'BD Execucao Cronograma Contratada'



class StageCronogramaContratadaCurva(models.Model):
    execucao = models.ForeignKey(ExecucaoCronoContratadas, on_delete=models.CASCADE, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT, blank=True, null=True)
    contratada = models.ForeignKey(CronogramaContratada, on_delete=models.PROTECT, blank=True, null=True)
    data_corte = models.DateField(blank=True, null=True)
    activity_id = models.CharField(max_length= 200, blank=True, null=True)
    resource_name = models.CharField(max_length= 200, blank=True, null=True)
    resource_type = models.CharField(max_length= 200, blank=True, null=True)
    spreadsheet_field = models.CharField(max_length= 200, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    valor = models.DecimalField(max_digits=38, decimal_places=5, blank=True, null=True)
    unidade = models.CharField(max_length= 200, blank=True, null=True)

    class Meta:
        db_table = 'cronograma_curva_contratada'
        verbose_name_plural = 'BD Stage Cronograma Contratada Curva'
        verbose_name = 'BD Stage Cronograma Contratada Curva'


class ConfiguraCronogramaContratada(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    activity_id = models.CharField(max_length=200, blank=True, null=True, default="Activity ID")
    resource_name = models.CharField(max_length=200, blank=True, null=True, default="Resource Name")
    resource_type = models.CharField(max_length=200, blank=True, null=True, default="Resource Type")
    spreadsheet_field = models.CharField(max_length=200, blank=True, null=True, default="Spreadsheet Field")
    planilha = models.CharField(max_length=200, blank=True, null=True, default="Curva")
    linha = models.CharField(max_length=200, blank=True, null=True, default='0')
    coluna = models.CharField(max_length=200, blank=True, null=True, default='0')

    class Meta:
        db_table = 'contratada_configura_cronograma'
        verbose_name_plural = 'BD Configura Cronograma Contratada'
        verbose_name = 'BD Configura Cronograma Contratada'

    def __str__(self):
        return self.activity_id


class StageCronogramaContratadaAtividade(models.Model):
    execucao = models.ForeignKey(ExecucaoCronoContratadas, on_delete=models.CASCADE, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT, blank=True, null=True)
    contratada = models.ForeignKey(CronogramaContratada, on_delete=models.PROTECT, blank=True, null=True)
    data_corte = models.DateField(blank=True, null=True)

    activity_id = models.CharField(max_length= 200, blank=True, null=True)
    descricao = models.CharField(max_length= 600, blank=True, null=True)
    folga_livre = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    folga_total = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    duracao = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    avanco = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    previsto = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    actual = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    data_inicio_bl = models.DateField(blank=True, null=True)
    data_fim_bl = models.DateField(blank=True, null=True)
    data_inicio_reprogramado = models.DateField(blank=True, null=True)
    data_fim_reprogramado = models.DateField(blank=True, null=True)
    data_inicio_real = models.DateField(blank=True, null=True)
    data_fim_real = models.DateField(blank=True, null=True)
    work_package = models.CharField(max_length=200, blank=True, null=True)
    OP_WP = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'cronograma_atividade_contratada'
        verbose_name_plural = 'BD Stage Cronograma Contratada Atividade'
        verbose_name = 'BD Stage Cronograma Contratada Atividade'

    def __str__(self):
        return self.activity_id