from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from apps.core.models import Usuario_Unidade
from apps.projeto.models import Usuario_Projeto
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
    class Meta:
        model = Usuario_Unidade
        fields = ('unidade',)





class ProjetoUsuarioAddForm(forms.ModelForm):
    class Meta:
        model = Usuario_Projeto
        fields = ('projeto',)