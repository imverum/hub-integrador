from django import forms
import datetime
from apps.cronogramacontratadas.models import CronogramaContratada, ExecucaoCronoContratadas
from apps.fornecedores.models import Fornecedores


class CronogramaCrontratadaAddForm(forms.ModelForm):
    contratada = forms.ModelChoiceField(queryset=Fornecedores.objects.none(), required=True, label='Contratada')
    contratada.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = CronogramaContratada
        fields = ('contratada',)

    def __init__(self, *args, **kwargs):

        contratada_queryset = kwargs.pop('contratada_queryset', Fornecedores.objects.all())

        super(CronogramaCrontratadaAddForm, self).__init__(*args, **kwargs)

        self.fields['contratada'].queryset = contratada_queryset


class CronogramaContratadaFormCarga(forms.ModelForm):
    arquivo = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'id': 'id_arquivo_curva'}))

    data_corte = forms.DateField(
        label='Data Corte',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = ExecucaoCronoContratadas
        fields = ('arquivo', 'data_corte')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['data_corte'].widget.attrs['max'] = str(datetime.date.today())