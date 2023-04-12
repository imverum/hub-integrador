from django.db import models

from apps.core.models import Owner, Unidade
from apps.fornecedores.models import Fornecedores
from apps.projeto.models import Projeto
from apps.usuario.models import Profile


class ExecucaoMasterIndex(models.Model):
    arquivo = models.FileField(upload_to='media/', null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    data_corte = models.DateField(blank=True, null=True)
    data_execucao = models.DateTimeField(auto_now=True, blank=True, null=True)
    inicio = models.DateTimeField(blank=True, null=True)
    termino = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length= 200, blank=True, null=True)
    tipo = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'execucao_master_index'
        verbose_name_plural = 'BD Execucao Master Index'
        verbose_name = 'BD Execucao Master Index'


class StageMasterIndexCWA(models.Model):
    execucao = models.ForeignKey(ExecucaoMasterIndex, on_delete=models.PROTECT, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    data_corte = models.DateField(blank=True, null=True)
    data_execucao = models.DateField(blank=True, null=True)

    codigo_do_projeto = models.CharField(max_length=200, blank=True, null=True)
    codigo_cwa = models.CharField(max_length=200, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    coordenadas = models.CharField(max_length=200, blank=True, null=True)
    nivel_do_solo = models.CharField(max_length=200, blank=True, null=True)


    class Meta:
        db_table = 'master_index_cwa_Stage'
        verbose_name_plural = 'BD Stage Master Index CWA'
        verbose_name = 'BD Stage Master Index CWA'


class ConfiguraMasterIndexCWA(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)

    codigo_do_projeto = models.CharField(max_length=200, blank=True, null=True)
    codigo_cwa = models.CharField(max_length=200, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    coordenadas = models.CharField(max_length=200, blank=True, null=True)
    nivel_do_solo = models.CharField(max_length=200, blank=True, null=True)
    planilha = models.CharField(max_length=200, blank=True, null=True)
    linha = models.CharField(max_length=200, blank=True, null=True)
    coluna = models.CharField(max_length=200, blank=True, null=True)




    class Meta:
        db_table = 'configura_master_index_cwa'
        verbose_name_plural = 'BD Configura Master Index CWA'
        verbose_name = 'BD Configura Master Index CWA'

    def __str__(self):
        return self.projeto



class StageMasterIndexPacotes(models.Model):
    execucao = models.ForeignKey(ExecucaoMasterIndex, on_delete=models.PROTECT, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    data_corte = models.DateField(blank=True, null=True)
    data_execucao = models.DateField(blank=True, null=True)

    codigo_do_projeto = models.CharField(max_length= 200, blank=True, null=True)
    codigo_do_pacote = models.CharField(max_length= 200, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    contrato = models.CharField(max_length= 200, blank=True, null=True)
    cwa = models.CharField(max_length= 200, blank=True, null=True)
    cwp = models.CharField(max_length= 200, blank=True, null=True)
    subarea = models.CharField(max_length= 200, blank=True, null=True)
    disciplina = models.CharField(max_length= 200, blank=True, null=True)
    subdisciplina = models.CharField(max_length= 200, blank=True, null=True)
    tipo = models.CharField(max_length= 200, blank=True, null=True)
    status = models.CharField(max_length= 200, blank=True, null=True)
    custo = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    responsavel = models.CharField(max_length=200, blank=True, null=True)
    horas_estimadas = models.CharField(max_length=200, blank=True, null=True)


    class Meta:
        db_table = 'stage_master_index_pacotes'
        verbose_name_plural = 'BD Stage Master Index Pacotes'
        verbose_name = 'BD Stage Master Index Pacotes'

class ConfiguraMasterIndexPacotes(models.Model):
        owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
        unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, blank=True, null=True)
        projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)

        codigo_do_projeto = models.CharField(max_length=200, blank=True, null=True)
        codigo_do_pacote = models.CharField(max_length=200, blank=True, null=True)
        descricao = models.CharField(max_length=200, blank=True, null=True)
        contrato = models.CharField(max_length=200, blank=True, null=True)
        cwa = models.CharField(max_length=200, blank=True, null=True)
        cwp = models.CharField(max_length=200, blank=True, null=True)
        subarea = models.CharField(max_length=200, blank=True, null=True)
        disciplina = models.CharField(max_length=200, blank=True, null=True)
        subdisciplina = models.CharField(max_length=200, blank=True, null=True)
        tipo = models.CharField(max_length=200, blank=True, null=True)
        status = models.CharField(max_length=200, blank=True, null=True)
        custo = models.CharField(max_length=200, blank=True, null=True)
        responsavel = models.CharField(max_length=200, blank=True, null=True)
        horas_estimadas = models.CharField(max_length=200, blank=True, null=True)

        planilha = models.CharField(max_length=200, blank=True, null=True)
        linha = models.CharField(max_length=200, blank=True, null=True)
        coluna = models.CharField(max_length=200, blank=True, null=True)

        class Meta:
            db_table = 'configura_master_index_pacotes'
            verbose_name_plural = 'BD Configura Master Index Pacotes'
            verbose_name = 'BD Configura Master Index Pacotes'

        def __str__(self):
            return self.projeto


class LogProcessamentoMasterIndex(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoMasterIndex, on_delete=models.CASCADE, blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = 'log_processamento_master_index'
        verbose_name_plural = 'BD Log processamento Master Index'
        verbose_name = 'BD Log Master Index'

    def __str__(self):
        return self.projeto



class ADFMasterIndexCWA(models.Model):
    execucao = models.ForeignKey(ExecucaoMasterIndex, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        db_table = 'execucao_master_adf_cwa'
        verbose_name_plural = 'BD ADF CWA Master Index'
        verbose_name = 'BD ADF CWA Master Index'



class ADFMasterIndexPACOTES(models.Model):
    execucao = models.ForeignKey(ExecucaoMasterIndex, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        db_table = 'execucao_master_adf_pacotes'
        verbose_name_plural = 'BD ADF PACOTES Master Index'
        verbose_name = 'BD ADF PACOTES Master Index'