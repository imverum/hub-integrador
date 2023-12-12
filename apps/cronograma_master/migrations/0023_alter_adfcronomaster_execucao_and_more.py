# Generated by Django 4.1.7 on 2023-11-06 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cronograma_master', '0022_alter_adfcontainercronomastercronogramas_container_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adfcronomaster',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.execucaocronomaster'),
        ),
        migrations.AlterField(
            model_name='adfcronomastercronogramas',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.execucaocronomaster'),
        ),
        migrations.AlterField(
            model_name='logprocessamentocronogramamaster',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.execucaocronomaster'),
        ),
        migrations.AlterField(
            model_name='stagecronogramamaster',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.execucaocronomaster'),
        ),
        migrations.AlterField(
            model_name='stagecronogramamasterbaseline',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.execucaocronomaster'),
        ),
        migrations.AlterField(
            model_name='xeractvcode',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.execucaocronomaster'),
        ),
        migrations.AlterField(
            model_name='xeractvtype',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.execucaocronomaster'),
        ),
        migrations.AlterField(
            model_name='xercalendar',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.execucaocronomaster'),
        ),
        migrations.AlterField(
            model_name='xerproject',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.execucaocronomaster'),
        ),
        migrations.AlterField(
            model_name='xerprojwbs',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.execucaocronomaster'),
        ),
        migrations.AlterField(
            model_name='xerrsrc',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.execucaocronomaster'),
        ),
    ]
