from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Perfil

class PerfilSignalTest(TestCase):
    def test_creacion_perfil_automatico(self):
        usuario = User.objects.create_user(
            username='testuser',
            password='PasswordSeguro123'
        )
        # Verifica que exista el perfil vinculado al usuario creado
        self.assertTrue(Perfil.objects.filter(user=usuario).exists())
