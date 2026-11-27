from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    biografia = models.TextField(blank=True, null=True)
    link_web = models.URLField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatares/', blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Signal para crear o guardar el perfil automáticamente
@receiver(post_save, sender=User)
def crear_o_guardar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    else:
        # Asegura que si el perfil existe, se guarde al actualizar el usuario
        if hasattr(instance, 'perfil'):
            instance.perfil.save()
