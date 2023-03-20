# Generated by Django 4.1.7 on 2023-03-15 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projeto', '0004_usuario_projeto_unidade'),
        ('core', '0002_usuario_unidade'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExecucaoLD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivold', models.FileField(blank=True, null=True, upload_to='media/')),
                ('data_corte', models.DateField(blank=True, null=True)),
                ('inicio', models.DateTimeField(blank=True, null=True)),
                ('termino', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.owner')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projeto.projeto')),
                ('unidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.unidade')),
            ],
            options={
                'verbose_name': 'BD Execucao LD',
                'verbose_name_plural': 'BD Execucao LD',
                'db_table': 'dbo_execucao_ld',
            },
        ),
        migrations.CreateModel(
            name='StageLd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sk', models.IntegerField(blank=True, null=True)),
                ('documento', models.CharField(blank=True, max_length=200, null=True)),
                ('numero_contratada', models.CharField(blank=True, max_length=200, null=True)),
                ('empresa', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo_emissao_inicial', models.CharField(blank=True, max_length=200, null=True)),
                ('certifica_na_1a_emissao', models.BooleanField(blank=True, null=True)),
                ('data_emissão_inicial_prevista', models.DateField(blank=True, null=True)),
                ('data_emissão_inicial_reprogramada', models.DateField(blank=True, null=True)),
                ('status_ld', models.CharField(blank=True, max_length=200, null=True)),
                ('titulo', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo_documento', models.CharField(blank=True, max_length=200, null=True)),
                ('formato', models.CharField(blank=True, max_length=200, null=True)),
                ('paginas', models.IntegerField(blank=True, null=True)),
                ('a1_equivalente', models.DecimalField(blank=True, decimal_places=2, max_digits=200, null=True)),
                ('codigo_atividade', models.CharField(blank=True, max_length=200, null=True)),
                ('work_package_area', models.CharField(blank=True, max_length=200, null=True)),
                ('work_package', models.CharField(blank=True, max_length=200, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ged.execucaold')),
            ],
            options={
                'verbose_name': 'BD Stage LD',
                'verbose_name_plural': 'BD Stage LD',
                'db_table': 'db_stage_ld',
            },
        ),
        migrations.CreateModel(
            name='ConfiguraLd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sk', models.IntegerField(blank=True, null=True)),
                ('documento', models.CharField(blank=True, max_length=200, null=True)),
                ('numero_contratada', models.CharField(blank=True, max_length=200, null=True)),
                ('empresa', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo_emissao_inicial', models.CharField(blank=True, max_length=200, null=True)),
                ('certifica_na_1a_emissao', models.BooleanField(blank=True, null=True)),
                ('data_emissão_inicial_prevista', models.DateField(blank=True, null=True)),
                ('data_emissão_inicial_reprogramada', models.DateField(blank=True, null=True)),
                ('status_ld', models.CharField(blank=True, max_length=200, null=True)),
                ('titulo', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo_documento', models.CharField(blank=True, max_length=200, null=True)),
                ('formato', models.CharField(blank=True, max_length=200, null=True)),
                ('paginas', models.IntegerField(blank=True, null=True)),
                ('a1_equivalente', models.DecimalField(blank=True, decimal_places=2, max_digits=200, null=True)),
                ('codigo_atividade', models.CharField(blank=True, max_length=200, null=True)),
                ('work_package_area', models.CharField(blank=True, max_length=200, null=True)),
                ('work_package', models.CharField(blank=True, max_length=200, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.owner')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projeto.projeto')),
                ('unidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.unidade')),
            ],
            options={
                'verbose_name': 'BD Configura LD',
                'verbose_name_plural': 'BD Configura LD',
                'db_table': 'db_configura_ld',
            },
        ),
    ]