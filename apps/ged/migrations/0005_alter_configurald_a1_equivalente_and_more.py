# Generated by Django 4.1.7 on 2023-03-16 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ged', '0004_remove_configurald_certifica_na_1a_emissao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configurald',
            name='a1_equivalente',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='configurald',
            name='data_emissão_inicial_prevista',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='configurald',
            name='paginas',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='configurald',
            name='sk',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
