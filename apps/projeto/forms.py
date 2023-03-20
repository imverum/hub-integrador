from django import forms
from apps.projeto.models import Projeto




class ProjetoFormAdd(forms.ModelForm):
    projeto = forms.CharField()
    codigo_projeto = forms.CharField()
    inicio_projeto = forms.DateField(
        label='Inícion Projeto',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class':'form-control'}))
    termino_projeto = forms.DateField(
        label='Termino Projeto',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))

    projeto.widget.attrs.update({'class': 'form-control'})
    codigo_projeto.widget.attrs.update({'class': 'form-control'})
    descricao = forms.CharField(label='Descrição',widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}))

    class Meta:
        model = Projeto
        fields = ('projeto', 'codigo_projeto', 'descricao', 'inicio_projeto', 'termino_projeto')


class GEDFormCarga(forms.Form):
    ged = forms.FileField(label='GED')
    data_corte = forms.DateField(
        label='Data Corte',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class':'form-control'}))