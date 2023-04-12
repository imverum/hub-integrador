# Generated by Django 4.1.7 on 2023-04-11 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projeto', '0001_initial'),
        ('cronograma_master', '0003_xeractvcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xeractvcode',
            name='actv_code_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='xeractvcode',
            name='actv_code_type_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='xeractvcode',
            name='seq_num',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='XerUDFValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('udf_type_id', models.IntegerField(blank=True, null=True)),
                ('fk_id', models.IntegerField(blank=True, null=True)),
                ('proj_id', models.IntegerField(blank=True, null=True)),
                ('udf_text', models.CharField(blank=True, max_length=300, null=True)),
                ('udf_code_id', models.CharField(blank=True, max_length=300, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD XER UDFValue',
                'verbose_name_plural': 'BD XER UDFValue',
                'db_table': 'xer_udfvalue',
            },
        ),
        migrations.CreateModel(
            name='XerUDFType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('udf_type_id', models.IntegerField(blank=True, null=True)),
                ('table_name', models.CharField(blank=True, max_length=300, null=True)),
                ('udf_type_name', models.CharField(blank=True, max_length=300, null=True)),
                ('udf_type_label', models.CharField(blank=True, max_length=300, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD XER UDFType',
                'verbose_name_plural': 'BD XER UDFType',
                'db_table': 'xer_UDFType',
            },
        ),
        migrations.CreateModel(
            name='XerTaskPRED',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_pred_id', models.IntegerField(blank=True, null=True)),
                ('task_id', models.IntegerField(blank=True, null=True)),
                ('pred_task_id', models.IntegerField(blank=True, null=True)),
                ('proj_id', models.IntegerField(blank=True, null=True)),
                ('pred_proj_id', models.IntegerField(blank=True, null=True)),
                ('pred_type', models.CharField(blank=True, max_length=300, null=True)),
                ('lag_hr_cnt', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD XER TaskPRED',
                'verbose_name_plural': 'BD XER TaskPRED',
                'db_table': 'xer_taskpred',
            },
        ),
        migrations.CreateModel(
            name='XerTaskACTV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actv_code_id', models.IntegerField(blank=True, null=True)),
                ('parent_actv_code_id', models.CharField(blank=True, max_length=300, null=True)),
                ('actv_code_type_id', models.IntegerField(blank=True, null=True)),
                ('actv_code_name', models.CharField(blank=True, max_length=300, null=True)),
                ('short_name', models.CharField(blank=True, max_length=300, null=True)),
                ('seq_num', models.IntegerField(blank=True, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD XER TaskACTV',
                'verbose_name_plural': 'BD XER TaskACTV',
                'db_table': 'xer_taskactv',
            },
        ),
        migrations.CreateModel(
            name='XerTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(blank=True, null=True)),
                ('proj_id', models.IntegerField(blank=True, null=True)),
                ('wbs_id', models.IntegerField(blank=True, null=True)),
                ('clndr_id', models.IntegerField(blank=True, null=True)),
                ('phys_complete_pct', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('complete_pct_type', models.CharField(blank=True, max_length=300, null=True)),
                ('task_type', models.CharField(blank=True, max_length=300, null=True)),
                ('duration_type', models.CharField(blank=True, max_length=300, null=True)),
                ('status_code', models.CharField(blank=True, max_length=300, null=True)),
                ('task_code', models.CharField(blank=True, max_length=300, null=True)),
                ('task_name', models.CharField(blank=True, max_length=300, null=True)),
                ('total_float_hr_cnt', models.CharField(blank=True, max_length=300, null=True)),
                ('free_float_hr_cnt', models.CharField(blank=True, max_length=300, null=True)),
                ('remain_drtn_hr_cnt', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('act_work_qty', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('remain_work_qty', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('target_work_qty', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('target_drtn_hr_cnt', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('target_equip_qty', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('act_equip_qty', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('remain_equip_qty', models.DecimalField(blank=True, decimal_places=5, max_digits=38, null=True)),
                ('cstr_date', models.CharField(blank=True, max_length=300, null=True)),
                ('act_start_date', models.CharField(blank=True, max_length=300, null=True)),
                ('act_end_date', models.CharField(blank=True, max_length=300, null=True)),
                ('late_start_date', models.CharField(blank=True, max_length=300, null=True)),
                ('late_end_date', models.CharField(blank=True, max_length=300, null=True)),
                ('expect_end_date', models.CharField(blank=True, max_length=300, null=True)),
                ('early_start_date', models.CharField(blank=True, max_length=300, null=True)),
                ('early_end_date', models.CharField(blank=True, max_length=300, null=True)),
                ('restart_date', models.CharField(blank=True, max_length=300, null=True)),
                ('reend_date', models.CharField(blank=True, max_length=300, null=True)),
                ('target_start_date', models.CharField(blank=True, max_length=300, null=True)),
                ('target_end_date', models.CharField(blank=True, max_length=300, null=True)),
                ('rem_late_start_date', models.CharField(blank=True, max_length=300, null=True)),
                ('rem_late_end_date', models.CharField(blank=True, max_length=300, null=True)),
                ('cstr_type', models.CharField(blank=True, max_length=300, null=True)),
                ('suspend_date', models.CharField(blank=True, max_length=300, null=True)),
                ('resume_date', models.CharField(blank=True, max_length=300, null=True)),
                ('float_path', models.CharField(blank=True, max_length=300, null=True)),
                ('float_path_order', models.CharField(blank=True, max_length=300, null=True)),
                ('cstr_date2', models.CharField(blank=True, max_length=300, null=True)),
                ('cstr_type2', models.CharField(blank=True, max_length=300, null=True)),
                ('driving_path_flag', models.CharField(blank=True, max_length=300, null=True)),
                ('create_date', models.CharField(blank=True, max_length=300, null=True)),
                ('update_date', models.CharField(blank=True, max_length=300, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD XER Task',
                'verbose_name_plural': 'BD XER Task',
                'db_table': 'xer_task',
            },
        ),
        migrations.CreateModel(
            name='XerRSRC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rsrc_id', models.IntegerField(blank=True, null=True)),
                ('clndr_id', models.IntegerField(blank=True, null=True)),
                ('rsrc_seq_num', models.IntegerField(blank=True, null=True)),
                ('rsrc_name', models.CharField(blank=True, max_length=300, null=True)),
                ('rsrc_short_name', models.CharField(blank=True, max_length=300, null=True)),
                ('rsrc_title_name', models.CharField(blank=True, max_length=300, null=True)),
                ('cost_qty_type', models.CharField(blank=True, max_length=300, null=True)),
                ('actv_flag', models.CharField(blank=True, max_length=300, null=True)),
                ('auto_complete_act_flag', models.CharField(blank=True, max_length=300, null=True)),
                ('curr_id', models.IntegerField(blank=True, null=True)),
                ('rsrc_type', models.CharField(blank=True, max_length=300, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD XER RSRC',
                'verbose_name_plural': 'BD XER RSRC',
                'db_table': 'xer_rsrc',
            },
        ),
        migrations.CreateModel(
            name='XerProJWBS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wbs_id', models.IntegerField(blank=True, null=True)),
                ('proj_id', models.IntegerField(blank=True, null=True)),
                ('obs_id', models.IntegerField(blank=True, null=True)),
                ('seq_num', models.IntegerField(blank=True, null=True)),
                ('proj_node_flag', models.CharField(blank=True, max_length=300, null=True)),
                ('sum_data_flag', models.CharField(blank=True, max_length=300, null=True)),
                ('status_code', models.CharField(blank=True, max_length=300, null=True)),
                ('wbs_short_name', models.CharField(blank=True, max_length=300, null=True)),
                ('wbs_name', models.CharField(blank=True, max_length=300, null=True)),
                ('parent_wbs_id', models.IntegerField(blank=True, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD XER ProJWBS',
                'verbose_name_plural': 'BD XER ProJWBS',
                'db_table': 'xer_projwbs',
            },
        ),
        migrations.CreateModel(
            name='XerProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proj_id', models.IntegerField(blank=True, null=True)),
                ('proj_short_name', models.CharField(blank=True, max_length=300, null=True)),
                ('def_complete_pct_type', models.CharField(blank=True, max_length=300, null=True)),
                ('clndr_id', models.IntegerField(blank=True, null=True)),
                ('task_code_base', models.IntegerField(blank=True, null=True)),
                ('task_code_step', models.IntegerField(blank=True, null=True)),
                ('last_recalc_date', models.CharField(blank=True, max_length=300, null=True)),
                ('def_task_type', models.CharField(blank=True, max_length=300, null=True)),
                ('critical_path_type', models.CharField(blank=True, max_length=300, null=True)),
                ('last_baseline_update_date', models.CharField(blank=True, max_length=300, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD XER Project',
                'verbose_name_plural': 'BD XER Project',
                'db_table': 'xer_project',
            },
        ),
        migrations.CreateModel(
            name='XerCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clndr_id', models.IntegerField(blank=True, null=True)),
                ('default_flag', models.CharField(blank=True, max_length=300, null=True)),
                ('clndr_name', models.CharField(blank=True, max_length=300, null=True)),
                ('proj_id', models.CharField(blank=True, max_length=300, null=True)),
                ('base_clndr_id', models.CharField(blank=True, max_length=300, null=True)),
                ('last_chng_date', models.CharField(blank=True, max_length=300, null=True)),
                ('clndr_type', models.CharField(blank=True, max_length=300, null=True)),
                ('day_hr_cnt', models.CharField(blank=True, max_length=300, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD XER Calendar',
                'verbose_name_plural': 'BD XER Calendar',
                'db_table': 'xer_calendar',
            },
        ),
        migrations.CreateModel(
            name='XerActvType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actv_code_type_id', models.IntegerField(blank=True, null=True)),
                ('actv_short_len', models.IntegerField(blank=True, null=True)),
                ('seq_num', models.IntegerField(blank=True, null=True)),
                ('actv_code_type', models.CharField(blank=True, max_length=300, null=True)),
                ('proj_id', models.CharField(blank=True, max_length=300, null=True)),
                ('actv_code_type_scope', models.CharField(blank=True, max_length=300, null=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cronograma_master.execucaocronomaster')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.projeto')),
            ],
            options={
                'verbose_name': 'BD XER ActvType',
                'verbose_name_plural': 'BD XER ActvType',
                'db_table': 'xer_actvtype',
            },
        ),
    ]