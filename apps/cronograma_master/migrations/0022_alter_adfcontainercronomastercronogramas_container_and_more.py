# Generated by Django 4.1.7 on 2023-06-05 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cronograma_master', '0021_execucaocronomaster_tipo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adfcontainercronomastercronogramas',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='stagecronogramamaster',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='stagecronogramamasterbaseline',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='xeractvcode',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='xeractvtype',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='xercalendar',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='xerproject',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='xerprojwbs',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='xerrsrc',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='xertask',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='xertaskactv',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='xertaskpred',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='xerudftype',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
        migrations.AlterField(
            model_name='xerudfvalue',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cronograma_master.containercronomaster'),
        ),
    ]
