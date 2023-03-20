from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings

from apps.core.models import Owner

ROLE_CHOICE=(
    (1,'Administrador'),
    (2,'Usuário'),
)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    nome = models.CharField(max_length=300, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    user_photo = models.ImageField(blank=True, null=True)
    role = models.IntegerField(choices=ROLE_CHOICE, default=2)


    class Meta:
        db_table = 'db_profile'
        verbose_name_plural = 'BD Profile'
        verbose_name = 'BD Profile'


    def __str__(self):
        return self.nome

