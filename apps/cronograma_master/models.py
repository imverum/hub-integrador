from django.db import models

from apps.core.models import Owner, Unidade
from apps.fornecedores.models import Fornecedores
from apps.projeto.models import Projeto
from apps.usuario.models import Profile


class ExecucaoCronoMaster(models.Model):
    arquivo = models.FileField(upload_to='media/', null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    data_execucao = models.DateTimeField(auto_now=True, blank=True, null=True)
    inicio = models.DateTimeField(blank=True, null=True)
    termino = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length= 200, blank=True, null=True)


    class Meta:
        db_table = 'execucao_cronograma_master'
        verbose_name_plural = 'BD Execucao Cronograma Master'
        verbose_name = 'BD Execucao Cronograma Master'

class StageCronogramaMaster(models.Model):
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.PROTECT, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    activity_id = models.CharField(max_length= 200, blank=True, null=True)
    resource_name = models.CharField(max_length= 200, blank=True, null=True)
    resource_type = models.CharField(max_length= 200, blank=True, null=True)
    spreadsheet_field = models.CharField(max_length= 200, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    valor = models.DecimalField(max_digits=38, decimal_places=5, blank=True, null=True)
    unidade = models.CharField(max_length= 200, blank=True, null=True)

    class Meta:
        db_table = 'cronograma_master_stage_curva'
        verbose_name_plural = 'BD Stage Cronograma Master'
        verbose_name = 'BD Stage Cronograma Master'

class ConfiguraCronogramaMaster(models.Model):
        owner = models.ForeignKey(Owner, on_delete=models.PROTECT, blank=True, null=True)
        unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, blank=True, null=True)
        projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
        activity_id = models.CharField(max_length=200, blank=True, null=True)
        resource_name = models.CharField(max_length=200, blank=True, null=True)
        resource_type = models.CharField(max_length=200, blank=True, null=True)
        spreadsheet_field = models.CharField(max_length=200, blank=True, null=True)
        planilha = models.CharField(max_length=200, blank=True, null=True)
        linha = models.CharField(max_length=200, blank=True, null=True)
        coluna = models.CharField(max_length=200, blank=True, null=True)

        class Meta:
            db_table = 'configura_cronograma_master'
            verbose_name_plural = 'BD Configura Cronograma Master'
            verbose_name = 'BD Configura Cronograma Master'

        def __str__(self):
            return self.activity_id


class LogProcessamentoCronogramaMaster(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = 'log_processamento_cronograma_master'
        verbose_name_plural = 'BD Log processamento Cronograma Master'
        verbose_name = 'BD Log Cronograma Master'

    def __str__(self):
        return self.projeto



class ADFCronoMaster(models.Model):
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        db_table = 'execucao_cronograma_master_adf'
        verbose_name_plural = 'BD Execucao Cronograma Master ADF'
        verbose_name = 'BD Execucao Cronograma Master ADF'





class XerActvcode(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)
    actv_code_id = models.IntegerField(blank=True, null=True)
    parent_actv_code_id = models.CharField(max_length=300, blank=True, null=True)
    actv_code_type_id = models.IntegerField(blank=True, null=True)
    actv_code_name = models.CharField(max_length=300, blank=True, null=True)
    short_name = models.CharField(max_length=300, blank=True, null=True)
    seq_num = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'XER.ACTVCODE'
        verbose_name_plural = 'BD XER Actvcode'
        verbose_name = 'BD XER Actvcode'


    def __str__(self):
        return self.projeto


class XerActvType(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)

    actv_code_type_id = models.IntegerField(blank=True, null=True)
    actv_short_len = models.IntegerField( blank=True, null=True)
    seq_num = models.IntegerField(blank=True, null=True)
    actv_code_type = models.CharField(max_length=300, blank=True, null=True)
    proj_id = models.CharField(max_length=300, blank=True, null=True)
    actv_code_type_scope = models.CharField(max_length=300, blank=True, null=True)


    class Meta:
        db_table = 'XER.ACTVTYPE'
        verbose_name_plural = 'BD XER ActvType'
        verbose_name = 'BD XER ActvType'


    def __str__(self):
        return self.projeto


class XerCalendar(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)

    clndr_id = models.IntegerField(blank=True, null=True)
    default_flag = models.CharField(max_length=300,blank=True, null=True)
    clndr_name = models.CharField(max_length=300,blank=True, null=True)
    proj_id = models.CharField(max_length=300, blank=True, null=True)
    base_clndr_id = models.CharField(max_length=300, blank=True, null=True)
    last_chng_date = models.CharField(max_length=300, blank=True, null=True)
    clndr_type = models.CharField(max_length=300, blank=True, null=True)
    day_hr_cnt = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = 'XER.CALENDAR'
        verbose_name_plural = 'BD XER Calendar'
        verbose_name = 'BD XER Calendar'


    def __str__(self):
        return self.projeto


class XerProject(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)

    proj_id = models.IntegerField(blank=True, null=True)
    proj_short_name = models.CharField(max_length=300,blank=True, null=True)
    def_complete_pct_type = models.CharField(max_length=300,blank=True, null=True)
    clndr_id = models.IntegerField(blank=True, null=True)
    task_code_base = models.IntegerField(blank=True, null=True)
    task_code_step = models.IntegerField(blank=True, null=True)
    last_recalc_date = models.CharField(max_length=300, blank=True, null=True)
    def_task_type = models.CharField(max_length=300, blank=True, null=True)
    critical_path_type = models.CharField(max_length=300, blank=True, null=True)
    last_baseline_update_date = models.CharField(max_length=300, blank=True, null=True)


    class Meta:
        db_table = 'XER.PROJECT'
        verbose_name_plural = 'BD XER Project'
        verbose_name = 'BD XER Project'


    def __str__(self):
        return self.projeto


class XerProJWBS(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)

    wbs_id = models.IntegerField(blank=True, null=True)
    proj_id = models.IntegerField(blank=True, null=True)
    obs_id = models.IntegerField(blank=True, null=True)
    seq_num = models.IntegerField(blank=True, null=True)
    proj_node_flag = models.CharField(max_length=300, blank=True, null=True)
    sum_data_flag = models.CharField(max_length=300, blank=True, null=True)
    status_code = models.CharField(max_length=300, blank=True, null=True)
    wbs_short_name = models.CharField(max_length=300, blank=True, null=True)
    wbs_name = models.CharField(max_length=300, blank=True, null=True)
    parent_wbs_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'XER.PROJWBS'
        verbose_name_plural = 'BD XER ProJWBS'
        verbose_name = 'BD XER ProJWBS'


    def __str__(self):
        return self.projeto


class XerRSRC(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)

    rsrc_id = models.IntegerField(blank=True, null=True)
    clndr_id = models.IntegerField(blank=True, null=True)
    rsrc_seq_num = models.IntegerField(blank=True, null=True)
    rsrc_name = models.CharField(max_length=300, blank=True, null=True)
    rsrc_short_name = models.CharField(max_length=300, blank=True, null=True)
    rsrc_title_name = models.CharField(max_length=300, blank=True, null=True)
    cost_qty_type = models.CharField(max_length=300, blank=True, null=True)
    actv_flag = models.CharField(max_length=300, blank=True, null=True)
    auto_complete_act_flag = models.CharField(max_length=300, blank=True, null=True)
    curr_id = models.IntegerField(blank=True, null=True)
    rsrc_type = models.CharField(max_length=300, blank=True, null=True)


    class Meta:
        db_table = 'XER.RSRC'
        verbose_name_plural = 'BD XER RSRC'
        verbose_name = 'BD XER RSRC'


    def __str__(self):
        return self.projeto


class XerTask(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)

    task_id = models.IntegerField(blank=True, null=True)
    proj_id = models.IntegerField(blank=True, null=True)
    wbs_id = models.IntegerField(blank=True, null=True)
    clndr_id = models.IntegerField(blank=True, null=True)
    phys_complete_pct = models.DecimalField(max_digits=38, decimal_places= 5 ,blank=True, null=True)
    complete_pct_type = models.CharField(max_length=300, blank=True, null=True)
    task_type = models.CharField(max_length=300, blank=True, null=True)
    duration_type = models.CharField(max_length=300, blank=True, null=True)
    status_code = models.CharField(max_length=300, blank=True, null=True)
    task_code = models.CharField(max_length=300, blank=True, null=True)
    task_name = models.CharField(max_length=300, blank=True, null=True)
    total_float_hr_cnt = models.CharField(max_length=300, blank=True, null=True)
    free_float_hr_cnt = models.CharField(max_length=300, blank=True, null=True)
    remain_drtn_hr_cnt = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    act_work_qty = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    remain_work_qty = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    target_work_qty = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    target_drtn_hr_cnt = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    target_equip_qty = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    act_equip_qty = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    remain_equip_qty = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)
    cstr_date = models.CharField(max_length=300, blank=True, null=True)
    act_start_date = models.CharField(max_length=300, blank=True, null=True)
    act_end_date = models.CharField(max_length=300, blank=True, null=True)
    late_start_date = models.CharField(max_length=300, blank=True, null=True)
    late_end_date = models.CharField(max_length=300, blank=True, null=True)
    expect_end_date = models.CharField(max_length=300, blank=True, null=True)
    early_start_date = models.CharField(max_length=300, blank=True, null=True)
    early_end_date = models.CharField(max_length=300, blank=True, null=True)
    restart_date = models.CharField(max_length=300, blank=True, null=True)
    reend_date = models.CharField(max_length=300, blank=True, null=True)
    target_start_date = models.CharField(max_length=300, blank=True, null=True)
    target_end_date = models.CharField(max_length=300, blank=True, null=True)
    rem_late_start_date = models.CharField(max_length=300, blank=True, null=True)
    rem_late_end_date = models.CharField(max_length=300, blank=True, null=True)
    cstr_type = models.CharField(max_length=300, blank=True, null=True)
    suspend_date = models.CharField(max_length=300, blank=True, null=True)
    resume_date = models.CharField(max_length=300, blank=True, null=True)
    float_path = models.CharField(max_length=300, blank=True, null=True)
    float_path_order = models.CharField(max_length=300, blank=True, null=True)
    cstr_date2 = models.CharField(max_length=300, blank=True, null=True)
    cstr_type2 = models.CharField(max_length=300, blank=True, null=True)
    driving_path_flag = models.CharField(max_length=300, blank=True, null=True)
    create_date = models.CharField(max_length=300, blank=True, null=True)
    update_date = models.CharField(max_length=300, blank=True, null=True)


    class Meta:
        db_table = 'XER.TASK'
        verbose_name_plural = 'BD XER Task'
        verbose_name = 'BD XER Task'


    def __str__(self):
        return self.projeto


class XerTaskACTV(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)

    task_id = models.IntegerField(blank=True, null=True)
    actv_code_type_id = models.IntegerField(blank=True, null=True)
    actv_code_id = models.IntegerField(blank=True, null=True)
    proj_id = models.IntegerField(blank=True, null=True)


    class Meta:
        db_table = 'XER.TASKACTV'
        verbose_name_plural = 'BD XER TaskACTV'
        verbose_name = 'BD XER TaskACTV'


    def __str__(self):
        return self.projeto


class XerTaskPRED(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)

    task_pred_id = models.IntegerField(blank=True, null=True)
    task_id = models.IntegerField(blank=True, null=True)
    pred_task_id = models.IntegerField(blank=True, null=True)
    proj_id = models.IntegerField(blank=True, null=True)
    pred_proj_id = models.IntegerField(blank=True, null=True)
    pred_type = models.CharField(max_length=300, blank=True, null=True)
    lag_hr_cnt = models.DecimalField(max_digits= 38, decimal_places= 5, blank=True, null=True)

    class Meta:
        db_table = 'XER.TASKPRED'
        verbose_name_plural = 'BD XER TaskPRED'
        verbose_name = 'BD XER TaskPRED'


    def __str__(self):
        return self.projeto

class XerUDFType(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)

    udf_type_id = models.IntegerField(blank=True, null=True)
    table_name = models.CharField(max_length=300, blank=True, null=True)
    udf_type_name = models.CharField(max_length=300, blank=True, null=True)
    udf_type_label = models.CharField(max_length=300, blank=True, null=True)




    class Meta:
        db_table = 'XER.UDFTYPE'
        verbose_name_plural = 'BD XER UDFType'
        verbose_name = 'BD XER UDFType'


    def __str__(self):
        return self.projeto


class XerUDFValue(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.CASCADE, blank=True, null=True)

    udf_type_id = models.IntegerField(blank=True, null=True)
    fk_id = models.IntegerField(blank=True, null=True)
    proj_id = models.IntegerField(blank=True, null=True)
    udf_text = models.CharField(max_length=300, blank=True, null=True)
    udf_code_id = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = 'XER.UDFVALUE'
        verbose_name_plural = 'BD XER UDFValue'
        verbose_name = 'BD XER UDFValue'

    def __str__(self):
        return self.projeto


class ADFCronoMasterCronogramas(models.Model):
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.PROTECT, blank=True, null=True)
    arquivo = models.CharField(max_length=300, blank=True, null=True)
    status_execucao_adf = models.CharField(max_length=200, blank=True, null=True, default='Concluído')
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        db_table = 'execucao_cronograma_master_cronogramas_adf'
        verbose_name_plural = 'BD Execucao Cronograma Master Cronogramas ADF'
        verbose_name = 'BD Execucao Cronograma Master Cronogramas ADF'




class StageCronogramaMasterBaseline(models.Model):
    execucao = models.ForeignKey(ExecucaoCronoMaster, on_delete=models.PROTECT, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, blank=True, null=True)

    codigo = models.CharField(max_length= 200, blank=True, null=True)
    descricao_atividade = models.CharField(max_length= 200, blank=True, null=True)
    inicio = models.CharField(max_length= 200, blank=True, null=True)
    termino = models.CharField(max_length= 200, blank=True, null=True)
    duracao = models.CharField(max_length= 200, blank=True, null=True)


    class Meta:
        db_table = 'cronograma_master_stage_baseline'
        verbose_name_plural = 'BD Stage Cronograma Master Baseline'
        verbose_name = 'BD Stage Cronograma Master Baseline'