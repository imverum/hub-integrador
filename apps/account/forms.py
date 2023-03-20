from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from apps.usuario.models import Profile, ROLE_CHOICE


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label= 'Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    email = forms.EmailField()
    password.widget.attrs.update({'class': 'form-control'})
    password2.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('O Passowrds salvo estão different')
        return cd['password2']
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email já cadastrado no sistema')
        return email

class UserProfileRegistrationForm(forms.ModelForm):
    nome = forms.CharField()
    nome.widget.attrs.update({'class': 'form-control'})
    role = forms.ChoiceField(choices=ROLE_CHOICE)
    role.widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Profile
        fields = ('nome', 'role')

#criando o inline
RegisterFormset = inlineformset_factory(
    User,
    Profile,
    form = UserProfileRegistrationForm,
    extra=0,
    can_delete=False,
    min_num=1,
    validate_min=True,
)


class UserProfileEditFormAdmin(forms.ModelForm):
    role = forms.ChoiceField(choices=ROLE_CHOICE)
    role.widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Profile
        fields = ('role',)

class UserEditFormAdmin(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active',)


#criando o inline
EditAdminFormset = inlineformset_factory(
    User,
    Profile,
    form = UserProfileEditFormAdmin,
    extra=0,
    can_delete=False,
    min_num=1,
    validate_min=True,
)