from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostCRUDTests(TestCase):

    def setUp(self):
        # Crear un usuario de prueba para asociarlo al campo autor
        self.usuario = User.objects.create_user(
            username='roberto',
            password='password123'
        )

    def test_crear_post_exitosamente(self):
        # Iniciar sesión en el cliente de prueba si la vista lo requiere
        self.client.login(username='roberto', password='password123')

        datos_post = {
            'titulo': 'Mi primer post de prueba',
            'subtitulo': 'Subtítulo del post',
            'contenido': 'Texto completo del post para validar el test automatizado.',
            'autor': self.usuario.id,   # ID del usuario requerido
            'estado': 'publicado',       # o 'borrador' / el valor que use tu choices
        }

        url = reverse('crear_post')  # Reemplazá por el name de tu URL si difiere
        respuesta = self.client.post(url, data=datos_post)

        # Validaciones
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().titulo, 'Mi primer post de prueba')
