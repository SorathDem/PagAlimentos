from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    ROLES = (
        ('fundacion', 'Fundación'),
        ('entidad', 'Entidad'),
        ('otro', 'Otro'),  # Puedes agregar más roles
    )
    rol = models.CharField(max_length=20, choices=ROLES, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"

from django.contrib.auth import get_user_model

User = get_user_model()

CATEGORIAS = [
    ('lacteos', 'Lácteos'),
    ('enlatados', 'Enlatados'),
    ('granos', 'Granos'),
    ('harinas', 'Harinas'),
]

User = get_user_model()

CATEGORIAS = [
    ('lacteos', 'Lácteos'),
    ('enlatados', 'Enlatados'),
    ('granos', 'Granos'),
    ('harinas', 'Harinas'),
]

class Publicacion(models.Model):
    entidad = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_empresa = models.CharField(max_length=255)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_empresa} - {self.fecha_publicacion.date()}"


class ProductoDonado(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='productos')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    fecha_caducidad = models.DateField()

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"
    
ESTADOS_SOLICITUD = [
    ('pendiente', 'Pendiente'),
    ('aprobada', 'Aprobada'),
    ('rechazada', 'Rechazada'),
]

class Solicitud(models.Model):
    fundacion = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes')
    publicacion = models.ForeignKey('Publicacion', on_delete=models.CASCADE, related_name='solicitudes')
    motivo = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADOS_SOLICITUD, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud de {self.fundacion} - {self.estado} - {self.publicacion.nombre_empresa}"

class ProductoSolicitado(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='productos_solicitados')
    producto = models.ForeignKey(ProductoDonado, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()