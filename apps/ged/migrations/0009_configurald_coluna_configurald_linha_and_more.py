# Generated by Django 4.1.7 on 2023-03-24 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ged', '0008_remove_configurald_sk_remove_stageld_sk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='configurald',
            name='coluna',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='configurald',
            name='linha',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='configurald',
            name='planilha',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
