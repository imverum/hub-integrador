from django.db import models

from apps.core.models import Owner, Unidade
from apps.fornecedores.models import Fornecedores
from apps.projeto.models import Projeto
from apps.usuario.models import Profile

ROLE_CHOICE_GED=(
    (1,'SIM'),
    (2,'NÃO'),
)


class FluxoEmissao(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    sigla_tipo_emissao = models.CharField(max_length= 200, blank=True, null=True)
    tipo_emissão = models.CharField(max_length= 200, blank=True, null=True)
    certifica_primeira_emissão = models.IntegerField(choices=ROLE_CHOICE_GED, default=2)
    cancelado = models.IntegerField(choices=ROLE_CHOICE_GED, default=2)


    class Meta:
        db_table = 'dbo_fluxo_emissao'
        verbose_name_plural = 'BD Fluxo Emissao'
        verbose_name = 'BD Fluxo Emissao'

class ExecucaoLD(models.Model):
    arquivold = models.FileField(upload_to='media/', null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedores, on_delete=models.CASCADE, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
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
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    documento = models.CharField(max_length= 200, blank=True, null=True)
    numero_contratada = models.CharField(max_length= 200, blank=True, null=True)
    empresa = models.CharField(max_length= 200, blank=True, null=True)
    tipo_emissao_inicial = models.CharField(max_length= 200, blank=True, null=True)
    certifica_na_1a_emissao = models.CharField(max_length= 200, blank=True, null=True)
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
        unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, blank=True, null=True)
        projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
        documento = models.CharField(max_length=200, blank=True, null=True)
        numero_contratada = models.CharField(max_length=200, blank=True, null=True)
        titulo = models.CharField(max_length=200, blank=True, null=True)
        status_ld = models.CharField(max_length=200, blank=True, null=True)
        codigo_atividade = models.CharField(max_length=200, blank=True, null=True)
        data_emissão_inicial_prevista = models.CharField(max_length=200, blank=True, null=True)
        paginas = models.CharField(max_length=200, blank=True, null=True)
        a1_equivalente = models.CharField(max_length=200, blank=True, null=True)
        tipo_emissao = models.CharField(max_length=200, blank=True, null=True)
        planilha = models.CharField(max_length=200, blank=True, null=True)
        linha = models.CharField(max_length=200, blank=True, null=True)
        coluna = models.CharField(max_length=200, blank=True, null=True)

        class Meta:
            db_table = 'db_configura_ld'
            verbose_name_plural = 'BD Configura LD'
            verbose_name = 'BD Configura LD'

        def __str__(self):
            return self.documento


class lod_processamento(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoLD, on_delete=models.CASCADE, blank=True, null=True)
    tipo = models.CharField(max_length=200, blank=True, null=True)
    log = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'db_log_processamento_ld'
        verbose_name_plural = 'BD Log processamento LD'
        verbose_name = 'BD Log processamento LD'

    def __str__(self):
        return self.tipo


class StageGED(models.Model):
    execucao = models.ForeignKey(ExecucaoLD, on_delete=models.PROTECT, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    documento_revisao = models.CharField(max_length= 200, blank=True, null=True)
    documento = models.CharField(max_length= 200, blank=True, null=True)
    revisao = models.CharField(max_length= 200, blank=True, null=True)
    certificado = models.CharField(max_length=200, blank=True, null=True)
    tipo_emissao = models.CharField(max_length=200, blank=True, null=True)
    cancelado = models.CharField(max_length=200, blank=True, null=True)
    tipo_documento = models.CharField(max_length=200, blank=True, null=True)
    disciplina = models.CharField(max_length=200, blank=True, null=True)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    empresa = models.CharField(max_length=200, blank=True, null=True)
    numero_contratada = models.CharField(max_length=200, blank=True, null=True)
    status_ged = models.CharField(max_length=200, blank=True, null=True)
    data_atualizacao = models.DateField(blank=True, null=True)
    ged_recebimento = models.CharField(max_length=200, blank=True, null=True)
    data_grd_recebimento = models.DateField(blank=True, null=True)
    data_analise = models.DateField(blank=True, null=True)
    resultado_analise = models.CharField(max_length=200, blank=True, null=True)
    e_certificadora = models.CharField(max_length=200, blank=True, null=True)
    grd_devolucao = models.CharField(max_length=200, blank=True, null=True)
    formato = models.CharField(max_length=200, blank=True, null=True)
    paginas = models.CharField(max_length=200, blank=True, null=True)
    a1_equivalente = models.CharField(max_length=200, blank=True, null=True)
    responsavel = models.CharField(max_length=200, blank=True, null=True)
    codigo_atividade = models.CharField(max_length=200, blank=True, null=True)
    work_package_area = models.CharField(max_length=200, blank=True, null=True)
    work_package = models.CharField(max_length=200, blank=True, null=True)
    rev_num = models.CharField(max_length=200, blank=True, null=True)


    class Meta:
        db_table = 'db_stage_ged'
        verbose_name_plural = 'BD Stage GED'
        verbose_name = 'BD Stage GED'

    def __str__(self):
        return self.documento

class ConfiguraGED(models.Model):
        owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)
        unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, blank=True, null=True)
        projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
        documento = models.CharField(max_length=200, blank=True, null=True)
        revisao = models.CharField(max_length=200, blank=True, null=True)
        tipo_documento = models.CharField(max_length=200, blank=True, null=True)
        disciplina = models.CharField(max_length=200, blank=True, null=True)
        titulo_1 = models.CharField(max_length=200, blank=True, null=True)
        titulo_2 = models.CharField(max_length=200, blank=True, null=True)
        empresa = models.CharField(max_length=200, blank=True, null=True)
        numero_contratada = models.CharField(max_length=200, blank=True, null=True)
        status_ged = models.CharField(max_length=200, blank=True, null=True)
        data_atualizacao = models.CharField(max_length=200, blank=True, null=True)
        grd_recebimento = models.CharField(max_length=200, blank=True, null=True)
        data_grd_recebimento = models.CharField(max_length=200, blank=True, null=True)
        data_analise = models.CharField(max_length=200, blank=True, null=True)
        resultado_analise = models.CharField(max_length=200, blank=True, null=True)
        formato = models.CharField(max_length=200, blank=True, null=True)
        work_package_area = models.CharField(max_length=200, blank=True, null=True)
        work_package = models.CharField(max_length=200, blank=True, null=True)
        tipo_emissao = models.CharField(max_length=200, blank=True, null=True)
        atual_responsavel = models.CharField(max_length=200, blank=True, null=True)
        planilha = models.CharField(max_length=200, blank=True, null=True)
        linha = models.CharField(max_length=200, blank=True, null=True)
        coluna = models.CharField(max_length=200, blank=True, null=True)


        class Meta:
            db_table = 'db_configura_ged'
            verbose_name_plural = 'BD Configura GED'
            verbose_name = 'BD Configura GED'

        def __str__(self):
            return self.documento



class FluxoDevolucaoGED(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)
    sigla_devolucao = models.CharField(max_length= 200, blank=True, null=True)
    certificado = models.IntegerField(choices=ROLE_CHOICE_GED, default=2)
    cancelado = models.IntegerField(choices=ROLE_CHOICE_GED, default=2)


    class Meta:
        db_table = 'dbo_fluxo_devolucao_ged'
        verbose_name_plural = 'BD Fluxo Devolucao GED'
        verbose_name = 'BD Fluxo Devolucao GED'