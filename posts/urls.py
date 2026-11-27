from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("acerca/", views.acerca, name="acerca"),
    path("contacto/", views.contacto, name="contacto"),
    path("posts/", views.lista_posts, name="lista_posts"),
    path("posts/nuevo/", views.crear_post, name="crear_post"),
    path("posts/<int:pk>/", views.detalle_post, name="detalle_post"),
    path("posts/<int:pk>/editar/", views.editar_post, name="editar_post"),
    path("posts/<int:pk>/eliminar/", views.eliminar_post, name="eliminar_post"),
]

from django.test import TestCase
from django.urls import reverse

class RutasProtegidasTest(TestCase):
    def test_crear_post_requiere_login(self):
        url = reverse('crear_post')  # Ajustá al name exacto de tu URL
        response = self.client.get(url)
        
        # Debe responder con una redirección (código 302)
        self.assertEqual(response.status_code, 302)
        
        # Verifica que la redirección apunte al login incluyendo el parámetro ?next=
        login_url = reverse('login')
        self.assertIn(login_url, response.url)
