"""
URL configuration for alimentos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from alimentosAPP import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', RedirectView.as_view(url='/index/')),
    path('admin/', admin.site.urls),
    path('adminPanel/', views.admin_panel, name='adminPanel'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # Gestión de publicaciones
    path('admin_publicaciones/', views.lista_publicaciones_admin, name='lista_publicaciones_admin'),
    path('editar_publicacion_admin/<int:pub_id>/', views.editar_publicacion_admin, name='editar_publicacion_admin'),
    path('eliminar_publicacion/<int:pub_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('producto_editar/<int:producto_id>/', views.editar_producto_donado, name='editar_producto_donado'),
    path('producto_eliminar/<int:producto_id>/', views.eliminar_producto_donado, name='eliminar_producto_donado'),
    path('reporte/donaciones-exitosas/', views.reporte_donaciones_exitosas, name='reporte_donaciones_exitosas'),
    path('reporte/donaciones-general/', views.reporte_donaciones_general, name='reporte_donaciones_general'),


    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),




    path('index/', views.principal, name='principal'),
    path('pagprincipal/', views.pagprincipal, name='pagprincipal'),
    path('fundacion/', views.vista_fundacion, name='fundacion'),
    path('entidad/', views.vista_entidad, name='entidad'),
    path('inicio/', views.pagprincipal, name='pagprincipal'),
    
    path('publicacion/nueva/', views.crear_publicacion, name='crear_publicacion'),
    path('mis-publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),
    path('publicaciones/', views.lista_publicaciones, name='lista_publicaciones'),
    path('editar_publicacion/<int:pk>/', views.editar_publicacion_usuario, name='editar_publicacion'),
    path('eliminar_publicacion_usuario/<int:pk>/', views.eliminar_publicacion_usuario, name='eliminar_publicacion_usuario'),
    path('solicitar/<int:publicacion_id>/', views.enviar_solicitud, name='enviar_solicitud'),
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('solicitud/<int:solicitud_id>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('solicitudes/<int:solicitud_id>/aprobar/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('solicitudes-fundacion/', views.solicitudes_fundacion, name='solicitudes_fundacion'),
    path('publicacion/<int:pk>/', views.detalle_publicacion, name='detalle_publicacion'),
    path('contactar/<int:publicacion_id>/', views.contactar_entidad, name='contactar_entidad'),

]

