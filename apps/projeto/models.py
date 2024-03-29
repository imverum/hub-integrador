from django.contrib.auth.models import User
from django.db import models

from apps.core.models import Owner, Unidade

ROLE_CHOICE_EXECUCAO=(
    (1, 'FEL 1'),
    (2, 'FEL 2'),
    (3, 'FEL 3'),
    (4, 'EXECUÇÃO'),
)

class Projeto(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, blank=True, null=True)
    projeto = models.CharField(max_length=300, blank=True, null=True)
    codigo_projeto = models.CharField(max_length=300, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    inicio_projeto = models.DateField(blank=True, null=True)
    termino_projeto = models.DateField(blank=True, null=True)
    awp_master_index = models.BooleanField(default=False)
    cronograma_master = models.BooleanField(default=False)
    cronograma_contratadas = models.BooleanField(default=False)
    bim = models.BooleanField(default=False)
    ged = models.BooleanField(default=False)
    suprimentos = models.BooleanField(default=False)
    gestao_materiais = models.BooleanField(default=False)
    comissionamento = models.BooleanField(default=False)
    fase = models.IntegerField(choices=ROLE_CHOICE_EXECUCAO, default=1)
    ativo = models.BooleanField(default=True)


    class Meta:
        db_table = 'projetos'
        verbose_name_plural = 'BD Projetos'
        verbose_name = 'BD Projetos'


    def __str__(self):
        return self.projeto

class Usuario_Projeto(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete= models.CASCADE)
    usuario = models.ForeignKey(User, on_delete= models.CASCADE)
    unidade = models.ForeignKey(Unidade, on_delete= models.CASCADE)


    class Meta:
        db_table = 'projeto_usuario'
        verbose_name_plural = 'DB Projeto Usuario'
        verbose_name = 'DB Projeto Usuario'