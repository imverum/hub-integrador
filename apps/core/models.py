from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Owner(models.Model):
    owner = models.CharField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True)


    def __str__(self):
        return self.owner

    class Meta:
        db_table = 'owner'
        verbose_name_plural = 'DB Unidade'
        verbose_name = 'DB Unidade'

class Unidade(models.Model):
    unidade = models.CharField(max_length=100)
    owner = models.ForeignKey(Owner, on_delete= models.PROTECT)
    photo = models.ImageField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    total_projetos = models.IntegerField(blank=True, null=True)
    total_user = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('list_unidade')

    def __str__(self):
        return self.unidade

    class Meta:
        db_table = 'unidade'
        verbose_name_plural = 'DB Unidade'
        verbose_name = 'DB Unidade'


class Usuario_Unidade(models.Model):
    unidade = models.ForeignKey(Unidade, on_delete= models.CASCADE)
    usuario = models.ForeignKey(User,on_delete= models.CASCADE)


    class Meta:
        db_table = 'unidade_usuario'
        verbose_name_plural = 'DB Unidade Usuario'
        verbose_name = 'DB Unidade Usuario'