from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from apps.core.models import Usuario_Unidade, Unidade
from apps.projeto.models import Usuario_Projeto, Projeto
from apps.usuario.models import Profile



class UserProfileRegistrationForm(forms.ModelForm):
    nome = forms.CharField()
    date_of_birth = forms.DateField(
        label='Data de naiscimento',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class':'form-control'}))

    nome.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Profile
        fields = ('nome', 'date_of_birth')



class UserProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label='Data de naiscimento',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    class Meta:
         model = Profile
         fields = ('date_of_birth', 'user_photo')


RegisterFormset = inlineformset_factory(
    User,
    Profile,
    form = UserProfileRegistrationForm,
    extra=0,
    can_delete=False,
    min_num=1,
    validate_min=True,
)



class UserEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label='Data de naiscimento',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    class Meta:
         model = Profile
         fields = ('nome', 'user_photo', 'date_of_birth')



class UnidadeAddForm(forms.ModelForm):
    unidade = forms.ModelChoiceField(queryset=Unidade.objects.none())
    unidade.widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Usuario_Unidade
        fields = ('unidade',)

    def __init__(self, *args, **kwargs):
        unidades_queryset = kwargs.pop('unidades_queryset', Unidade.objects.all())
        super().__init__(*args, **kwargs)
        self.fields['unidade'].queryset = unidades_queryset





class ProjetoUsuarioAddForm(forms.ModelForm):
    projeto = forms.ModelChoiceField(queryset=Projeto.objects.none())
    projeto.widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Usuario_Projeto
        fields = ('projeto',)

    def __init__(self, *args, **kwargs):
        projetos_queryset = kwargs.pop('projetos_queryset', Projeto.objects.all())
        super().__init__(*args, **kwargs)
        self.fields['projeto'].queryset = projetos_queryset