from django.db import models

from apps.projeto.models import Projeto


class ControleBOMCompras(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    arquivo = models.FileField(upload_to='media/', null=True, blank=True)

    data_execucao = models.DateTimeField(auto_now=True, blank=True, null=True)
    data_corte = models.DateTimeField(blank=True, null=True)

    projeto_bom = models.CharField(max_length=200, blank=True, null=True)
    cwa = models.CharField(max_length=200, blank=True, null=True)
    disciplina = models.CharField(max_length=200, blank=True, null=True)
    cwp = models.CharField(max_length=200, blank=True, null=True)
    iwp = models.CharField(max_length=200, blank=True, null=True)
    position_status = models.CharField(max_length=200, blank=True, null=True)
    issue_status = models.CharField(max_length=200, blank=True, null=True)
    codigo_padrao_fornecedor = models.CharField(max_length=200, blank=True, null=True)
    descritivo_curto = models.CharField(max_length=200, blank=True, null=True)
    descritivo_longo = models.CharField(max_length=500, blank=True, null=True)
    tipo_material = models.CharField(max_length=500, blank=True, null=True)
    quantidade = models.DecimalField(max_digits= 38, decimal_places= 2, blank=True, null=True)
    unidade = models.CharField(max_length=500, blank=True, null=True)
    ros_date = models.DateField(blank=True, null=True)
    peso_unitario = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    desenho_vale_montagem = models.CharField(max_length=500, blank=True, null=True)
    proc_pack = models.CharField(max_length=500, blank=True, null=True)
    pacote_fornecimento = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'controlecompras_bom'
        verbose_name_plural = 'BD Execucao BOM'
        verbose_name = 'BD Execucao BOM'


