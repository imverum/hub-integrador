from django.db import models

from apps.core.models import Owner


class Fornecedores(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    fornecedor = models.CharField(max_length= 200, blank=True, null=True)
    cnpj = models.CharField(max_length= 200, blank=True, null=True)
    estado = models.CharField(max_length= 2, blank=True, null=True)
    pais = models.CharField(max_length= 100, blank=True, null=True)
    cep = models.CharField(max_length= 30, blank=True, null=True)
    bairro = models.CharField(max_length= 100, blank=True, null=True)
    cidade = models.CharField(max_length= 100, blank=True, null=True)
    rua = models.CharField(max_length= 200, blank=True, null=True)
    descricao = models.CharField(max_length= 200, blank=True, null=True)

    class Meta:
        db_table = 'dbo_fornecedor'
        verbose_name_plural = 'BD Fornecedor'
        verbose_name = 'BD Fornecedor'

    def __str__(self):
        return self.fornecedor


class FornecedoresRepresentante(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedores, on_delete=models.PROTECT, blank=True, null=True)
    representante = models.CharField(max_length= 200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contato = models.CharField(max_length= 11, blank=True, null=True)


    class Meta:
        db_table = 'dbo_fornecedor_representante'
        verbose_name_plural = 'BD Fornecedor Representante'
        verbose_name = 'BD Fornecedor Representante'

    def __str__(self):
        return self.representante