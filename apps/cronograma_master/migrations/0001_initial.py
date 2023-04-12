# Generated by Django 4.1.7 on 2023-04-06 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projeto', '0001_initial'),
        ('usuario', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExecucaoCronoMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(blank=True, null=True, upload_to='media/')),
                ('data_execucao', models.DateTimeField(auto_now=True, null=True)),
                ('inicio', models.DateTimeField(blank=True, null=True)),
                ('termino', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.owner')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.profile')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
                ('unidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.unidade')),
            ],
            options={
                'verbose_name': 'BD Execucao Cronograma Master',
                'verbose_name_plural': 'BD Execucao Cronograma Master',
                'db_table': 'execucao_cronograma_master',
            },
        ),
        migrations.CreateModel(
            name='StageCronogramaMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_id', models.CharField(blank=True, max_length=200, null=True)),
                ('resource_name', models.CharField(blank=True, max_length=200, null=True)),
                ('resource_type', models.CharField(blank=True, max_length=200, null=True)),
                ('spreadsheet_field', models.CharField(blank=True, max_length=200, null=True)),
                ('data', models.DateField(blank=True, null=True)),
                ('valor', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('unidade', models.CharField(blank=True, max_length=200, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD Stage Cronograma Master',
                'verbose_name_plural': 'BD Stage Cronograma Master',
                'db_table': 'cronograma_master_stage_curvaa',
            },
        ),
        migrations.CreateModel(
            name='LogProcessamentoCronogramaMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(blank=True, max_length=300, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD Log Cronograma Master',
                'verbose_name_plural': 'BD Log processamento Cronograma Master',
                'db_table': 'log_processamento_cronograma_master',
            },
        ),
        migrations.CreateModel(
            name='ConfiguraCronogramaMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_id', models.CharField(blank=True, max_length=200, null=True)),
                ('resource_name', models.CharField(blank=True, max_length=200, null=True)),
                ('resource_type', models.CharField(blank=True, max_length=200, null=True)),
                ('spreadsheet_field', models.CharField(blank=True, max_length=200, null=True)),
                ('planilha', models.CharField(blank=True, max_length=200, null=True)),
                ('linha', models.CharField(blank=True, max_length=200, null=True)),
                ('coluna', models.CharField(blank=True, max_length=200, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.owner')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
                ('unidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.unidade')),
            ],
            options={
                'verbose_name': 'BD Configura Cronograma Master',
                'verbose_name_plural': 'BD Configura Cronograma Master',
                'db_table': 'configura_cronograma_master',
            },
        ),
        migrations.CreateModel(
            name='ADFCronoMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cronograma_master.execucaocronomaster')),
            ],
            options={
                'verbose_name': 'BD Execucao Cronograma Master ADF',
                'verbose_name_plural': 'BD Execucao Cronograma Master ADF',
                'db_table': 'execucao_cronograma_master_adf',
            },
        ),
    ]
