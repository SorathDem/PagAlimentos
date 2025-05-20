from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import PublicacionForm, ProductoDonadoForm
from .models import ProductoDonado, Publicacion
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .models import Publicacion, CATEGORIAS
from django.views.decorators.http import require_POST
from .models import Publicacion, ProductoDonado, Solicitud, ProductoSolicitado
from .models import CustomUser, Publicacion, ProductoDonado
from .forms import PublicacionForm, ProductoDonadoForm
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from .forms import ProductoDonadoFormSet

# Create your views here.
def principal(request):
    return render(request, "index.html")

def pagprincipal(request):
    return render(request, "pagprincipal.html")

def admin_panel(request):
    return render(request, 'admin_panel.html')


def vista_entidad(request):
    return render(request, 'entidad_panel.html')


def vista_fundacion(request):
    return render(request, 'fundacion_panel.html')

def logout_view(request):
    logout(request)
    return redirect('principal')

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirección según rol
            if user.rol == 'fundacion':
                return redirect('fundacion')
            elif user.rol == 'entidad':
                return redirect('entidad')
            elif user.is_superuser:
                return redirect('adminPanel')
            else:
                return redirect('pagprincipal')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'registration/login.html')


@login_required
def crear_publicacion(request):
    ProductoFormSet = modelformset_factory(ProductoDonado, form=ProductoDonadoForm, extra=1, can_delete=True)

    if request.method == 'POST':
        pub_form = PublicacionForm(request.POST)
        formset = ProductoFormSet(request.POST, queryset=ProductoDonado.objects.none())

        if pub_form.is_valid() and formset.is_valid():
            publicacion = pub_form.save(commit=False)
            publicacion.entidad = request.user
            publicacion.save()

            for form in formset:
                if form.cleaned_data:
                    producto = form.save(commit=False)
                    producto.publicacion = publicacion
                    producto.save()

            return redirect('mis_publicaciones')  # Ruta a la lista de publicaciones
    else:
        pub_form = PublicacionForm()
        formset = ProductoFormSet(queryset=ProductoDonado.objects.none())

    return render(request, 'crear_publicacion.html', {
        'pub_form': pub_form,
        'formset': formset
    })

def editar_publicacion_usuario(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)

    if request.method == 'POST':
        pub_form = PublicacionForm(request.POST, instance=publicacion)
        formset = ProductoDonadoFormSet(request.POST, instance=publicacion)

        if pub_form.is_valid() and formset.is_valid():
            pub_form.save()
            formset.save()
            return redirect('lista_publicaciones')
    else:
        pub_form = PublicacionForm(instance=publicacion)
        formset = ProductoDonadoFormSet(instance=publicacion)

    return render(request, 'editar_publicacion_usuario.html', {'pub_form': pub_form, 'formset': formset})

def eliminar_publicacion_usuario(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)

    if request.method == 'POST':
        publicacion.delete()
        messages.success(request, 'Publicación eliminada correctamente.')
        return redirect('lista_publicaciones')  # Cambia por la URL que uses

    return render(request, 'confirmar_eliminacion.html', {'publicacion': publicacion})

@login_required
def mis_publicaciones(request):
    publicaciones = Publicacion.objects.filter(entidad=request.user)
    return render(request, 'mis_publicaciones.html', {'publicaciones': publicaciones})

def lista_publicaciones(request):
    publicaciones = Publicacion.objects.all().prefetch_related('productos')
    return render(request, 'lista_publicaciones.html', {
        'publicaciones': publicaciones,
        'categorias': CATEGORIAS,
    })

@login_required
@require_POST
def enviar_solicitud(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    motivo = request.POST.get('motivo')
    
    solicitud = Solicitud.objects.create(
        fundacion=request.user,
        publicacion=publicacion,
        motivo=motivo
    )

    for producto in publicacion.productos.all():
        cantidad = request.POST.get(f'producto_{producto.id}')
        if cantidad:
            cantidad = int(cantidad)
            if cantidad > 0:
               ProductoSolicitado.objects.create(
                    solicitud=solicitud,
                    producto=producto,
                    cantidad=cantidad
                )


    return redirect('lista_publicaciones')

def lista_solicitudes(request):
    solicitudes = Solicitud.objects.select_related('fundacion').all().order_by('-fecha_solicitud')

    return render(request, 'lista_solicitudes.html', {'solicitudes': solicitudes})


def detalle_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, id=pk)
    productos = publicacion.productos.all()
    return render(request, 'detalle_publicacion.html', {
        'publicacion': publicacion,
        'productos': productos,
    })
    
def detalle_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    productos_solicitados = solicitud.productos_solicitados.select_related('producto').all()

    return render(request, 'detalle_solicitud.html', {
        'solicitud': solicitud,
        'productos_solicitados': productos_solicitados,
    })

def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    if solicitud.estado == "Aprobada":
        messages.warning(request, "Esta solicitud ya fue aprobada.")
        return redirect('lista_solicitudes')

    productos = solicitud.productos_solicitados.select_related('producto').all()
    
    for ps in productos:
        producto = ps.producto
        if producto.cantidad >= ps.cantidad:
            producto.cantidad -= ps.cantidad
            producto.save()
        else:
            messages.error(request, f"No hay suficiente cantidad para el producto {producto.nombre}.")
            return redirect('lista_solicitudes')

    solicitud.estado = "Aprobada"
    solicitud.save()
    messages.success(request, "Solicitud aprobada correctamente.")
    return redirect('lista_solicitudes')


User = get_user_model()

@login_required
@user_passes_test(lambda u: u.is_superuser)
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = CustomUserCreationForm()
    return render(request, 'crear_usuario.html', {'form': form})


@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = CustomUserCreationForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    usuario.delete()
    return redirect('lista_usuarios')


# ADMINISTRAR PUBLICACIONES
@login_required
@user_passes_test(lambda u: u.is_superuser)
def lista_publicaciones_admin(request):
    publicaciones = Publicacion.objects.all().prefetch_related('productos')
    return render(request, 'admin_lista_publicaciones.html', {'publicaciones': publicaciones})

def editar_publicacion_admin(request, pub_id):
    publicacion = get_object_or_404(Publicacion, id=pub_id)
    productos = ProductoDonado.objects.filter(publicacion=publicacion)

    if request.method == 'POST':
        form = PublicacionForm(request.POST, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('lista_publicaciones_admin')
    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, 'editar_publicacion_admin.html', {
        'form': form,
        'publicacion': publicacion,
        'productos': productos,
    })

    
@login_required
def eliminar_publicacion(request, pub_id):
    publicacion = get_object_or_404(Publicacion, id=pub_id)
    publicacion.delete()
    return redirect('lista_publicaciones_admin')

def editar_producto_donado(request, producto_id):
    producto = get_object_or_404(ProductoDonado, id=producto_id)
    publicacion = producto.publicacion
    productos_publicacion = ProductoDonado.objects.filter(publicacion=publicacion)

    if request.method == 'POST':
        form = ProductoDonadoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('editar_publicacion_admin', pub_id=publicacion.id)
    else:
        form = ProductoDonadoForm(instance=producto)

    return render(request, 'editar_producto_admin.html', {
        'form': form,
        'producto': producto,
        'publicacion': publicacion,
        'productos_publicacion': productos_publicacion,
    })

def eliminar_producto_donado(request, producto_id):
    producto = get_object_or_404(ProductoDonado, id=producto_id)
    publicacion_id = producto.publicacion.id
    producto.delete()
    return redirect('editar_publicacion_admin', pub_id=publicacion_id)


def reporte_donaciones_exitosas(request):
    # Traemos las solicitudes aprobadas con prefetch de productos solicitados y productos donados
    donaciones = Solicitud.objects.filter(estado="Aprobada").prefetch_related(
        'productos_solicitados__producto'
    )
    return render(request, 'reporte_donaciones_exitosas.html', {'donaciones': donaciones})

def reporte_donaciones_general(request):
    donaciones = Solicitud.objects.exclude(estado="Pendiente").prefetch_related(
        'productos_solicitados__producto'
    )
    return render(request, 'reporte_donaciones_general.html', {'donaciones': donaciones})

def solicitudes_fundacion(request):
    solicitudes = Solicitud.objects.filter(fundacion=request.user)
    return render(request, 'solicitudes_fundacion.html', {'solicitudes': solicitudes})

from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Publicacion
from django.contrib import messages

def contactar_entidad(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    destinatario = publicacion.entidad.email  # Corregido para obtener email desde entidad

    if request.method == 'POST':
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        remitente = request.user.email if request.user.is_authenticated else 'no-reply@tuapp.com'

        if asunto and mensaje:
            try:
                send_mail(
                    asunto,
                    mensaje,
                    remitente,
                    [destinatario],
                    fail_silently=False,
                )
                messages.success(request, 'Correo enviado correctamente.')
                return redirect('fundacion')  # Ajusta la URL destino según tu proyecto
            except Exception as e:
                messages.error(request, f'Error al enviar el correo: {e}')
        else:
            messages.error(request, 'Por favor completa todos los campos.')

    return render(request, 'contactar_entidad.html', {'publicacion': publicacion})

