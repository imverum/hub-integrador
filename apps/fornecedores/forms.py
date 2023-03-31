from django import forms

from apps.fornecedores.models import Fornecedores



class FornecedorRegisterForm(forms.ModelForm):
    fornecedor = forms.CharField()
    fornecedor.widget.attrs.update({'class': 'form-control'})

    cnpj = forms.CharField()
    cnpj.widget.attrs.update({'class': 'form-control'})

    pais = forms.CharField()
    pais.widget.attrs.update({'class': 'form-control'})

    estado = forms.CharField()
    estado.widget.attrs.update({'class': 'form-control'})

    bairro = forms.CharField()
    bairro.widget.attrs.update({'class': 'form-control'})

    rua = forms.CharField()
    rua.widget.attrs.update({'class': 'form-control'})

    cep = forms.CharField()
    cep.widget.attrs.update({'class': 'form-control'})

    descricao = forms.CharField()
    descricao.widget.attrs.update({'class': 'form-control'})

    cidade = forms.CharField()
    cidade.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Fornecedores
        fields = ('fornecedor', 'cnpj', 'pais', 'estado', 'bairro', 'cidade', 'rua', 'cep', 'descricao')