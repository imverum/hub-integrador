from django import forms


from apps.master_index.models import ExecucaoMasterIndex, ConfiguraMasterIndexCWA, ConfiguraMasterIndexPacotes


class PacotesFormCarga(forms.ModelForm):

    data_corte = forms.DateField(
        label='Data Corte',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = ExecucaoMasterIndex
        fields = ('arquivo', 'data_corte')

class CWAFormCarga(forms.ModelForm):

    data_corte = forms.DateField(
        label='Data Corte',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = ExecucaoMasterIndex
        fields = ('arquivo', 'data_corte')


class ConfiguraCWAForm(forms.ModelForm):
    codigo_do_projeto = forms.CharField()
    codigo_do_projeto.widget.attrs.update({'class': 'form-control'})

    codigo_cwa = forms.CharField()
    codigo_cwa.widget.attrs.update({'class': 'form-control'})

    descricao = forms.CharField()
    descricao.widget.attrs.update({'class': 'form-control'})

    coordenadas = forms.CharField()
    coordenadas.widget.attrs.update({'class': 'form-control'})

    nivel_do_solo = forms.CharField()
    nivel_do_solo.widget.attrs.update({'class': 'form-control'})

    planilha = forms.CharField()
    planilha.widget.attrs.update({'class': 'form-control'})

    linha = forms.CharField()
    linha.widget.attrs.update({'class': 'form-control'})

    coluna = forms.CharField()
    coluna.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ConfiguraMasterIndexCWA
        fields = ('codigo_do_projeto', 'codigo_cwa', 'descricao', 'coordenadas', 'nivel_do_solo','planilha', 'linha', 'coluna')


class ConfiguraPacotesForm(forms.ModelForm):
    codigo_do_projeto = forms.CharField()
    codigo_do_projeto.widget.attrs.update({'class': 'form-control'})

    codigo_do_pacote = forms.CharField()
    codigo_do_pacote.widget.attrs.update({'class': 'form-control'})

    descricao = forms.CharField()
    descricao.widget.attrs.update({'class': 'form-control'})

    contrato = forms.CharField()
    contrato.widget.attrs.update({'class': 'form-control'})


    cwa = forms.CharField()
    cwa.widget.attrs.update({'class': 'form-control'})

    cwp = forms.CharField()
    cwp.widget.attrs.update({'class': 'form-control'})

    subarea = forms.CharField()
    subarea.widget.attrs.update({'class': 'form-control'})

    disciplina = forms.CharField()
    disciplina.widget.attrs.update({'class': 'form-control'})

    subdisciplina = forms.CharField()
    subdisciplina.widget.attrs.update({'class': 'form-control'})

    tipo = forms.CharField()
    tipo.widget.attrs.update({'class': 'form-control'})

    status = forms.CharField()
    status.widget.attrs.update({'class': 'form-control'})

    custo = forms.CharField()
    custo.widget.attrs.update({'class': 'form-control'})

    responsavel = forms.CharField()
    responsavel.widget.attrs.update({'class': 'form-control'})

    horas_estimadas = forms.CharField()
    horas_estimadas.widget.attrs.update({'class': 'form-control'})

    planilha = forms.CharField()
    planilha.widget.attrs.update({'class': 'form-control'})

    linha = forms.CharField()
    linha.widget.attrs.update({'class': 'form-control'})

    coluna = forms.CharField()
    coluna.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ConfiguraMasterIndexPacotes
        fields = ('codigo_do_projeto', 'codigo_do_pacote', 'descricao', 'contrato',  'cwa','cwp', 'subarea','disciplina', 'subdisciplina', 'tipo', 'status', 'custo', 'responsavel', 'horas_estimadas', 'planilha', 'linha', 'coluna')
