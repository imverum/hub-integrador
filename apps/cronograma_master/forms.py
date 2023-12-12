from django import forms

from apps.cronograma_master.models import ExecucaoCronoMaster, ConfiguraCronogramaMaster


class CronogramaMasterBaselineFormCarga(forms.ModelForm):
    arquivo = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'id': 'id_arquivo_baseline'}))

    class Meta:
        model = ExecucaoCronoMaster
        fields = ('arquivo',)


class CronogramaMasterFormCarga(forms.ModelForm):
    arquivo = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'id': 'id_arquivo_curva'}))

    class Meta:
        model = ExecucaoCronoMaster
        fields = ('arquivo',)

class CronogramaMasterFormCargaXer(forms.Form):
    arquivo = forms.CharField()
    arquivo.widget.attrs.update({'class': 'form-control'})



class ConfiguraCronogramaMasterForm(forms.ModelForm):
    activity_id = forms.CharField()
    activity_id.widget.attrs.update({'class': 'form-control'})

    resource_name = forms.CharField()
    resource_name.widget.attrs.update({'class': 'form-control'})

    resource_type = forms.CharField()
    resource_type.widget.attrs.update({'class': 'form-control'})

    spreadsheet_field = forms.CharField()
    spreadsheet_field.widget.attrs.update({'class': 'form-control'})

    planilha = forms.CharField()
    planilha.widget.attrs.update({'class': 'form-control'})

    linha = forms.CharField()
    linha.widget.attrs.update({'class': 'form-control'})

    coluna = forms.CharField()
    coluna.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ConfiguraCronogramaMaster
        fields = ('activity_id', 'resource_name', 'resource_type', 'spreadsheet_field', 'planilha', 'linha', 'coluna')

class CronogramaMasterAvancoFormCarga(forms.Form):
    arquivo = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'id': 'id_arquivo'}))

