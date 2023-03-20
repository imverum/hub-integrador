from django import forms

from apps.ged.models import ExecucaoLD, ConfiguraLd


class LDFormCarga(forms.ModelForm):
    data_corte = forms.DateField(
        label='Data Corte',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    class Meta:
        model = ExecucaoLD
        fields = ('arquivold', 'data_corte' )




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

    sk = forms.CharField()
    sk.widget.attrs.update({'class': 'form-control'})

    data_emissão_inicial_prevista = forms.CharField()
    data_emissão_inicial_prevista.widget.attrs.update({'class': 'form-control'})

    paginas = forms.CharField()
    paginas.widget.attrs.update({'class': 'form-control'})

    a1_equivalente = forms.CharField()
    a1_equivalente.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ConfiguraLd
        fields = ('documento', 'numero_contratada', 'titulo', 'status_ld','codigo_atividade' ,'sk','data_emissão_inicial_prevista','paginas','a1_equivalente' )