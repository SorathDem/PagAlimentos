from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Publicacion, ProductoDonado
from django.forms import inlineformset_factory

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'rol', 'password1', 'password2')

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'rol', 'password1', 'password2']

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['nombre_empresa']

class ProductoDonadoForm(forms.ModelForm):
    fecha_caducidad = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ProductoDonado
        fields = ['nombre', 'cantidad', 'fecha_caducidad', 'categoria']

ProductoDonadoFormSet = inlineformset_factory(
    Publicacion,
    ProductoDonado,
    form=ProductoDonadoForm,
    extra=1,        # cuántos formularios vacíos adicionales mostrar
    can_delete=True # permite eliminar productos
)