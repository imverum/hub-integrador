# Generated by Django 4.1.7 on 2023-03-13 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projeto', '0002_projeto_ativo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario_Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DB Projeto Usuario',
                'verbose_name_plural': 'DB Projeto Usuario',
                'db_table': 'db_projeto_usuario',
            },
        ),
    ]
