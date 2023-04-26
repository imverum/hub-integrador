from django import forms

from apps.fornecedores.models import Fornecedores
from apps.ged.models import ExecucaoLD, ConfiguraLd, FluxoEmissao, ROLE_CHOICE_GED, FluxoDevolucaoGED

class GEDFormCarga(forms.ModelForm):

    data_corte = forms.DateField(
        label='Data Corte',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    arquivold = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'id': 'id_arquivo_ged'}))
    class Meta:
        model = ExecucaoLD
        fields = ('arquivold', 'data_corte')


class FluxoRegisterForm(forms.ModelForm):
    sigla_tipo_emissao = forms.CharField()
    sigla_tipo_emissao.widget.attrs.update({'class': 'form-control'})

    tipo_emissão = forms.CharField()
    tipo_emissão.widget.attrs.update({'class': 'form-control'})

    certifica_primeira_emissão = forms.ChoiceField(choices=ROLE_CHOICE_GED)
    certifica_primeira_emissão.widget.attrs.update({'class': 'form-control'})

    cancelado = forms.ChoiceField(choices=ROLE_CHOICE_GED)
    cancelado.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = FluxoEmissao
        fields = ('sigla_tipo_emissao', 'tipo_emissão', 'certifica_primeira_emissão', 'cancelado')
class LDFormCarga(forms.ModelForm):

    data_corte = forms.DateField(
        label='Data Corte',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))

    fornecedor = forms.ModelChoiceField(queryset=Fornecedores.objects.none())
    fornecedor.widget.attrs.update({'class': 'form-control'})
    arquivold = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'id': 'id_arquivo_ld'}))


    class Meta:
        model = ExecucaoLD
        fields = ('arquivold', 'data_corte', 'fornecedor')

    def __init__(self, *args, **kwargs):
        fornecedor_queryset = kwargs.pop('fornecedor_queryset', Fornecedores.objects.all())
        super().__init__(*args, **kwargs)
        self.fields['fornecedor'].queryset = fornecedor_queryset




class ConfiguraLdForm(forms.ModelForm):
    documento = forms.CharField()
    documento.widget.attrs.update({'class': 'form-control'})

    numero_contratada = forms.CharField()
    numero_contratada.widget.attrs.update({'class': 'form-control'})

    titulo = forms.CharField()
    titulo.widget.attrs.update({'class': 'form-control'})

    status_ld = forms.CharField()
    status_ld.widget.attrs.update({'class': 'form-control'})

    codigo_atividade = forms.CharField()
    codigo_atividade.widget.attrs.update({'class': 'form-control'})

    data_emissão_inicial_prevista = forms.CharField()
    data_emissão_inicial_prevista.widget.attrs.update({'class': 'form-control'})

    paginas = forms.CharField()
    paginas.widget.attrs.update({'class': 'form-control'})

    a1_equivalente = forms.CharField()
    a1_equivalente.widget.attrs.update({'class': 'form-control'})

    planilha = forms.CharField()
    planilha.widget.attrs.update({'class': 'form-control'})

    linha = forms.CharField()
    linha.widget.attrs.update({'class': 'form-control'})

    coluna = forms.CharField()
    coluna.widget.attrs.update({'class': 'form-control'})

    tipo_emissao = forms.CharField()
    tipo_emissao.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ConfiguraLd
        fields = ('documento', 'numero_contratada', 'titulo', 'status_ld','codigo_atividade' ,'data_emissão_inicial_prevista','paginas','a1_equivalente', 'tipo_emissao','planilha', 'linha', 'coluna')


class ConfiguraGEDForm(forms.ModelForm):
    documento = forms.CharField()
    documento.widget.attrs.update({'class': 'form-control'})

    revisao = forms.CharField()
    revisao.widget.attrs.update({'class': 'form-control'})

    tipo_documento = forms.CharField()
    tipo_documento.widget.attrs.update({'class': 'form-control'})

    disciplina = forms.CharField()
    disciplina.widget.attrs.update({'class': 'form-control'})

    titulo_1 = forms.CharField()
    titulo_1.widget.attrs.update({'class': 'form-control'})

    titulo_2 = forms.CharField()
    titulo_2.widget.attrs.update({'class': 'form-control'})

    empresa = forms.CharField()
    empresa.widget.attrs.update({'class': 'form-control'})

    numero_contratada = forms.CharField()
    numero_contratada.widget.attrs.update({'class': 'form-control'})

    status_ged = forms.CharField()
    status_ged.widget.attrs.update({'class': 'form-control'})

    data_atualizacao = forms.CharField()
    data_atualizacao.widget.attrs.update({'class': 'form-control'})

    grd_recebimento = forms.CharField()
    grd_recebimento.widget.attrs.update({'class': 'form-control'})

    data_grd_recebimento = forms.CharField()
    data_grd_recebimento.widget.attrs.update({'class': 'form-control'})

    data_analise= forms.CharField()
    data_analise.widget.attrs.update({'class': 'form-control'})

    resultado_analise = forms.CharField()
    resultado_analise.widget.attrs.update({'class': 'form-control'})

    formato = forms.CharField()
    formato.widget.attrs.update({'class': 'form-control'})

    work_package_area = forms.CharField()
    work_package_area.widget.attrs.update({'class': 'form-control'})

    work_package = forms.CharField()
    work_package.widget.attrs.update({'class': 'form-control'})

    tipo_emissao = forms.CharField()
    tipo_emissao.widget.attrs.update({'class': 'form-control'})

    atual_responsavel = forms.CharField()
    atual_responsavel.widget.attrs.update({'class': 'form-control'})

    planilha = forms.CharField()
    planilha.widget.attrs.update({'class': 'form-control'})

    linha = forms.CharField()
    linha.widget.attrs.update({'class': 'form-control'})

    coluna = forms.CharField()
    coluna.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ConfiguraLd
        fields = ('documento', 'revisao', 'tipo_documento', 'disciplina','titulo_1' ,'titulo_2','empresa','numero_contratada', 'status_ged','data_atualizacao', 'grd_recebimento', 'data_grd_recebimento',"data_analise", "resultado_analise", 'formato', 'work_package_area', 'work_package', 'tipo_emissao', 'atual_responsavel', 'planilha', 'linha', 'coluna')


class FluxoDevolucaoForm(forms.ModelForm):
    sigla_devolucao = forms.CharField()
    sigla_devolucao.widget.attrs.update({'class': 'form-control'})

    certificado = forms.ChoiceField(choices=ROLE_CHOICE_GED)
    certificado.widget.attrs.update({'class': 'form-control'})

    cancelado = forms.ChoiceField(choices=ROLE_CHOICE_GED)
    cancelado.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = FluxoDevolucaoGED
        fields = ('sigla_devolucao', 'certificado', 'cancelado')