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
            name='ExecucaoMasterIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(blank=True, null=True, upload_to='media/')),
                ('data_corte', models.DateField(blank=True, null=True)),
                ('data_execucao', models.DateTimeField(auto_now=True, null=True)),
                ('inicio', models.DateTimeField(blank=True, null=True)),
                ('termino', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo', models.CharField(blank=True, max_length=200, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.owner')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.profile')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
                ('unidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.unidade')),
            ],
            options={
                'verbose_name': 'BD Execucao Master Index',
                'verbose_name_plural': 'BD Execucao Master Index',
                'db_table': 'execucao_master_index',
            },
        ),
        migrations.CreateModel(
            name='StageMasterIndexPacotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_corte', models.DateField(blank=True, null=True)),
                ('data_execucao', models.DateField(blank=True, null=True)),
                ('codigo_do_projeto', models.CharField(blank=True, max_length=200, null=True)),
                ('codigo_do_pacote', models.CharField(blank=True, max_length=200, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('contrato', models.CharField(blank=True, max_length=200, null=True)),
                ('cwa', models.CharField(blank=True, max_length=200, null=True)),
                ('cwp', models.CharField(blank=True, max_length=200, null=True)),
                ('subarea', models.CharField(blank=True, max_length=200, null=True)),
                ('disciplina', models.CharField(blank=True, max_length=200, null=True)),
                ('subdisciplina', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('custo', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('responsavel', models.CharField(blank=True, max_length=200, null=True)),
                ('horas_estimadas', models.CharField(blank=True, max_length=200, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='master_index.execucaomasterindex')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD Stage Master Index Pacotes',
                'verbose_name_plural': 'BD Stage Master Index Pacotes',
                'db_table': 'stage_master_index_pacotes',
            },
        ),
        migrations.CreateModel(
            name='StageMasterIndexCWA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_corte', models.DateField(blank=True, null=True)),
                ('data_execucao', models.DateField(blank=True, null=True)),
                ('codigo_do_projeto', models.CharField(blank=True, max_length=200, null=True)),
                ('codigo_cwa', models.CharField(blank=True, max_length=200, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('coordenadas', models.CharField(blank=True, max_length=200, null=True)),
                ('nivel_do_solo', models.CharField(blank=True, max_length=200, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='master_index.execucaomasterindex')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD Stage Master Index CWA',
                'verbose_name_plural': 'BD Stage Master Index CWA',
                'db_table': 'master_index_cwa_Stage',
            },
        ),
        migrations.CreateModel(
            name='LogProcessamentoMasterIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(blank=True, max_length=300, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master_index.execucaomasterindex')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD Log Master Index',
                'verbose_name_plural': 'BD Log processamento Master Index',
                'db_table': 'log_processamento_master_index',
            },
        ),
        migrations.CreateModel(
            name='ConfiguraMasterIndexPacotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_do_projeto', models.CharField(blank=True, max_length=200, null=True)),
                ('codigo_do_pacote', models.CharField(blank=True, max_length=200, null=True)),
                ('descricao', models.CharField(blank=True, max_length=200, null=True)),
                ('contrato', models.CharField(blank=True, max_length=200, null=True)),
                ('cwa', models.CharField(blank=True, max_length=200, null=True)),
                ('cwp', models.CharField(blank=True, max_length=200, null=True)),
                ('subarea', models.CharField(blank=True, max_length=200, null=True)),
                ('disciplina', models.CharField(blank=True, max_length=200, null=True)),
                ('subdisciplina', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('custo', models.CharField(blank=True, max_length=200, null=True)),
                ('responsavel', models.CharField(blank=True, max_length=200, null=True)),
                ('horas_estimadas', models.CharField(blank=True, max_length=200, null=True)),
                ('planilha', models.CharField(blank=True, max_length=200, null=True)),
                ('linha', models.CharField(blank=True, max_length=200, null=True)),
                ('coluna', models.CharField(blank=True, max_length=200, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.owner')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
                ('unidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.unidade')),
            ],
            options={
                'verbose_name': 'BD Configura Master Index Pacotes',
                'verbose_name_plural': 'BD Configura Master Index Pacotes',
                'db_table': 'configura_master_index_pacotes',
            },
        ),
        migrations.CreateModel(
            name='ConfiguraMasterIndexCWA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_do_projeto', models.CharField(blank=True, max_length=200, null=True)),
                ('codigo_cwa', models.CharField(blank=True, max_length=200, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('coordenadas', models.CharField(blank=True, max_length=200, null=True)),
                ('nivel_do_solo', models.CharField(blank=True, max_length=200, null=True)),
                ('planilha', models.CharField(blank=True, max_length=200, null=True)),
                ('linha', models.CharField(blank=True, max_length=200, null=True)),
                ('coluna', models.CharField(blank=True, max_length=200, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.owner')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
                ('unidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.unidade')),
            ],
            options={
                'verbose_name': 'BD Configura Master Index CWA',
                'verbose_name_plural': 'BD Configura Master Index CWA',
                'db_table': 'configura_master_index_cwa',
            },
        ),
        migrations.CreateModel(
            name='ADFMasterIndexPACOTES',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='master_index.execucaomasterindex')),
            ],
            options={
                'verbose_name': 'BD ADF PACOTES Master Index',
                'verbose_name_plural': 'BD ADF PACOTES Master Index',
                'db_table': 'execucao_master_adf_pacotes',
            },
        ),
        migrations.CreateModel(
            name='ADFMasterIndexCWA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='master_index.execucaomasterindex')),
            ],
            options={
                'verbose_name': 'BD ADF CWA Master Index',
                'verbose_name_plural': 'BD ADF CWA Master Index',
                'db_table': 'execucao_master_adf_cwa',
            },
        ),
    ]
