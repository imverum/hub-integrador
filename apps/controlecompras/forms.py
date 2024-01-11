from django import forms
import datetime

from apps.controlecompras.models import ControleBOMCompras


from apps.fornecedores.models import Fornecedores



class BOMContratadaFormCarga(forms.ModelForm):
    arquivo = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'id': 'id_arquivo_curva'}))

    data_corte = forms.DateField(
        label='Data Corte',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = ControleBOMCompras
        fields = ('arquivo', 'data_corte')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['data_corte'].widget.attrs['max'] = str(datetime.date.today())