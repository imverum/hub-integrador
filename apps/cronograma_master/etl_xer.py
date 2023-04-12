from xerparser.reader import Reader
import io
from apps.cronograma_master.models import XerTask, XerCalendar, XerTaskPRED, XerActvcode, XerActvType, XerProject, \
    XerProJWBS, XerRSRC, XerUDFType, XerUDFValue, ADFCronoMasterCronogramas


def run_etl_xer (arquivo_file, projeto, crono, request):

    xer_file = Reader(arquivo_file)
    print(xer_file)
    carga_tabela_task(xer_file, projeto, crono)
    carga_tabela_calendar(xer_file, projeto, crono)
    carga_tabela_taskpred(xer_file, projeto, crono)
    carga_tabela_actvcode(xer_file, projeto, crono)
    carga_tabela_actvtype(xer_file, projeto, crono)
    carga_tabela_project(xer_file, projeto, crono)
    carga_tabela_projws(xer_file, projeto, crono)
    carga_tabela_rsrc(xer_file, projeto, crono)
    carga_tabela_udftypec(xer_file, projeto, crono)
    carga_tabela_udfvalue(xer_file, projeto, crono)
    carga_tabela_adf_crono(crono)

def carga_tabela_task(xer_file, projeto, crono):
    projeto_tasks = xer_file.activities
    print(projeto_tasks)
    for atividade in projeto_tasks:
        carga_xer_task = XerTask.objects.create(
        projeto = projeto,
        execucao = crono,
        task_id = int(atividade.task_id),
        proj_id = int(atividade.proj_id),
        wbs_id = int(atividade.wbs_id),
        clndr_id = int(atividade.clndr_id),
        phys_complete_pct = float(atividade.phys_complete_pct),
        complete_pct_type = str(atividade.complete_pct_type),
        task_type = str(atividade.task_type),
        duration_type = str(atividade.duration_type),
        status_code = str(atividade.status_code),
        task_code = str(atividade.task_code),
        task_name = str(atividade.task_name),
        total_float_hr_cnt = atividade.total_float_hr_cnt,
        free_float_hr_cnt = atividade.free_float_hr_cnt,
        remain_drtn_hr_cnt = float(atividade.remain_drtn_hr_cnt),
        act_work_qty = float(atividade.act_work_qty),
        remain_work_qty = float(atividade.remain_work_qty),
        target_work_qty = float(atividade.target_work_qty),
        target_drtn_hr_cnt = float(atividade.target_drtn_hr_cnt),
        target_equip_qty = float(atividade.target_equip_qty),
        act_equip_qty = float(atividade.act_equip_qty),
        remain_equip_qty = float(atividade.remain_equip_qty),
        cstr_date = atividade.cstr_date,
        act_start_date = atividade.act_start_date,
        act_end_date = atividade.act_end_date,
        late_start_date = atividade.late_start_date,
        late_end_date = atividade.late_end_date,
        expect_end_date = atividade.expect_end_date,
        early_start_date = atividade.early_start_date,
        early_end_date = atividade.early_end_date,
        restart_date = atividade.restart_date,
        reend_date = atividade.reend_date,
        target_start_date = atividade.target_start_date,
        target_end_date = atividade.target_end_date,
        rem_late_start_date = atividade.rem_late_start_date,
        rem_late_end_date = atividade.rem_late_end_date,
        cstr_type = str(atividade.cstr_type),
        suspend_date = atividade.suspend_date,
        resume_date = atividade.resume_date,
        float_path = str(atividade.int_path),
        float_path_order = str(atividade.int_path_order),
        cstr_date2 = atividade.cstr_date2,
        cstr_type2 = atividade.cstr_type2,
        driving_path_flag = atividade.driving_path_flag,
        create_date = atividade.create_date,
        update_date = atividade.update_date,
        )

def carga_tabela_calendar(xer_file, projeto, crono):
    projeto_calendar = xer_file.calendars
    for calendario in projeto_calendar:
        carga_xer_calendar = XerCalendar.objects.create(
        projeto=projeto,
        execucao=crono,
        clndr_id = int(calendario.clndr_id),
        default_flag = calendario.default_flag,
        clndr_name = str(calendario.clndr_name),
        proj_id = str(calendario.proj_id),
        base_clndr_id = calendario.base_clndr_id,
        last_chng_date = calendario.last_chng_date,
        clndr_type = str(calendario.clndr_type),
        day_hr_cnt = calendario.day_hr_cnt,
        )

def carga_tabela_taskpred(xer_file, projeto, crono):
    projeto_taskpred = xer_file.relations
    for relacionamento in projeto_taskpred:
        carga_xer_taskpred = XerTaskPRED.objects.create(
        projeto=projeto,
        execucao=crono,
        task_pred_id = int(relacionamento.task_pred_id),
        task_id = int(relacionamento.task_id),
        pred_task_id = int(relacionamento.pred_task_id),
        proj_id = int(relacionamento.proj_id),
        pred_proj_id = int(relacionamento.pred_proj_id),
        pred_type = str(relacionamento.pred_type),
        lag_hr_cnt = float(relacionamento.lag_hr_cnt),
        )

def carga_tabela_actvcode(xer_file, projeto, crono):
    # Tabela ACTVCODE
    projeto_actvcode = xer_file.actvcodes
    for codigo in projeto_actvcode:
        carga_xer_actvcode = XerActvcode.objects.create(
        projeto=projeto,
        execucao=crono,
        actv_code_id = int(codigo.actv_code_id),
        parent_actv_code_id = codigo.parent_actv_code_id,
        actv_code_type_id = int(codigo.actv_code_type_id),
        actv_code_name = str(codigo.actv_code_name),
        short_name = str(codigo.short_name),
        seq_num = int(codigo.seq_num),
        )

def carga_tabela_actvtype(xer_file, projeto, crono):
    # Tabela ACTVTYPE
    projeto_actvtype = xer_file.acttypes
    for codigo in projeto_actvtype:
        carga_xer_actvtype = XerActvType.objects.create(
        projeto=projeto,
        execucao=crono,
        actv_code_type_id = int(codigo.actv_code_type_id),
        actv_short_len = int(codigo.actv_short_len),
        seq_num = int(codigo.seq_num),
        actv_code_type = str(codigo.actv_code_type),
        proj_id = str(codigo.proj_id),
        actv_code_type_scope = str(codigo.actv_code_type_scope),
        )

def carga_tabela_project(xer_file, projeto_carga, crono):
    # Tabela PROJECT
    projeto_projects = xer_file.projects
    for projeto in projeto_projects:
        carga_xer_project = XerProject.objects.create(
        projeto=projeto_carga,
        execucao=crono,
        proj_id = int(projeto.proj_id),
        proj_short_name = str(projeto.proj_short_name),
        def_complete_pct_type = str(projeto.def_complete_pct_type),
        clndr_id = int(projeto.clndr_id),
        task_code_base = int(projeto.task_code_base),
        task_code_step = int(projeto.task_code_step),
        last_recalc_date = projeto.last_recalc_date,
        def_task_type = projeto.def_task_type,
        critical_path_type = projeto.critical_path_type,
        last_baseline_update_date = projeto.last_baseline_update_date,
        )

def carga_tabela_projws(xer_file, projeto, crono):
    # Tabela PROJWBS
    projeto_wbs = xer_file.wbss
    for wbs in projeto_wbs:
        carga_xer_projws = XerProJWBS.objects.create(
        projeto=projeto,
        execucao=crono,
        wbs_id = int(wbs.wbs_id),
        proj_id = int(wbs.proj_id),
        obs_id = int(wbs.obs_id),
        seq_num = int(wbs.seq_num),
        proj_node_flag = str(wbs.proj_node_flag),
        sum_data_flag = str(wbs.sum_data_flag),
        status_code = str(wbs.status_code),
        wbs_short_name = str(wbs.wbs_short_name),
        wbs_name = str(wbs.wbs_name),
        parent_wbs_id = int(wbs.parent_wbs_id),
        )

def carga_tabela_rsrc(xer_file, projeto, crono):
    # Tabela RSRC
    projeto_rsrc = xer_file.resources
    for recursos in projeto_rsrc:
        carga_xer_rsrc = XerRSRC.objects.create(
        projeto=projeto,
        execucao=crono,
        rsrc_id = int(recursos.rsrc_id),
        clndr_id = int(recursos.clndr_id),
        rsrc_seq_num = int(recursos.rsrc_seq_num),
        rsrc_name = str(recursos.rsrc_name),
        rsrc_short_name = str(recursos.rsrc_short_name),
        rsrc_title_name = str(recursos.rsrc_title_name),
        cost_qty_type = str(recursos.cost_qty_type),
        actv_flag = str(recursos.active_flag),
        auto_complete_act_flag = str(recursos.auto_compute_act_flag),
        curr_id = int(recursos.curr_id),
        rsrc_type = str(recursos.rsrc_type),
        )

def carga_tabela_udftypec(xer_file, projeto, crono):
    # Tabela UDFTYPE
    projeto_udftype = xer_file.udftypes
    for codigo in projeto_udftype:
        carga_xer_udftype = XerUDFType.objects.create(
        projeto=projeto,
        execucao=crono,
        udf_type_id = int(codigo.udf_type_id),
        table_name = str(codigo.table_name),
        udf_type_name = str(codigo.udf_type_name),
        udf_type_label = str(codigo.udf_type_label),
        )

def carga_tabela_udfvalue(xer_file, projeto, crono):
    # Tabela UDFVALUE
    projeto_udfvalue = xer_file.udfvalues
    for codigo in projeto_udfvalue:
        carga_xer_udfvalue = XerUDFValue.objects.create(
        projeto=projeto,
        execucao=crono,
        udf_type_id = int(codigo.udf_type_id),
        fk_id = int(codigo.fk_id),
        proj_id = int(codigo.proj_id),
        udf_text = str(codigo.udf_text),
        udf_code_id = str(codigo.udf_code_id),
        )


def carga_tabela_adf_crono(crono):
    carga_xer_adf_crono = ADFCronoMasterCronogramas.objects.create(
        execucao=crono,
        arquivo = "xer",
        )