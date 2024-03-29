# Generated by Django 4.1.7 on 2023-06-01 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0001_initial'),
        ('cronograma_master', '0020_execucaocronomaster_inicio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='execucaocronomaster',
            name='tipo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='stagecronogramamaster',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='stagecronogramamasterbaseline',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='xeractvcode',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='xeractvtype',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='xercalendar',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='xerproject',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='xerprojwbs',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='xerrsrc',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='xertask',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='xertaskactv',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='xertaskpred',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='xerudftype',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.AddField(
            model_name='xerudfvalue',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.containercronomaster'),
        ),
        migrations.CreateModel(
            name='ADFContainerCronoMasterCronogramas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_execucao_adf', models.CharField(blank=True, max_length=200, null=True)),
                ('container', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cronograma_master.containercronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD Execucao Container Master Cronogramas ADF',
                'verbose_name_plural': 'BD Execucao Container Master Cronogramas ADF',
                'db_table': 'execucao_cronograma_master_container_adf',
            },
        ),
    ]
