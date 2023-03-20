from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.contrib.auth.models import User
from datetime import datetime
from apps.usuario.models import Profile


class ProfileTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user('luiz@neurondat.com', 'luiz@neurondat.com', '123456789!@#a')
        self.profile = Profile.objects.create(user=self.user,nome='Luiz Arthur', date_of_birth=datetime.strptime('15/06/1990', '%d/%m/%Y').date(), whatsapp='719999999999')
        self.client.login(username='luiz@neurondat.com', password='123456789!@#a')
        self.response = self.client.get(r('profile_detail'))

    def test_get(self):

        """
        Retorna um status code 200
        """
        self.assertEqual(200, self.response.status_code)


    def test_template(self):
        """
        Retornando o template profile.html
        """
        self.assertTemplateUsed(self.response, 'profile.html')

    def test_context(self):

        varibles = ['usuario', 'profile', 'form']

        for key in varibles:
            with self.subTest():
               self.assertIn(key, self.response.context)




