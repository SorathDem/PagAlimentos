from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
# Create your views here.
def principal(request):
    return render(request, "index.html")

def pagprincipal(request):
    return render(request, "pagprincipal.html")

@login_required
def login_page(request):
   return render(request, 'login.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirigir_usuario(request)  # Redirige según el tipo de usuario
        else:
            return render(request, "login.html", {"error": "Usuario o contraseña incorrectos"})  

    return render(request, "login.html")

def redirigir_usuario(request):
    if request.user.is_superuser:
        return redirect('pagPrincipal')  # Redirige al panel de administración
    elif request.user.is_staff:
        return redirect('psicologo')  # Redirige a la página de psicólogos
    else:
        return redirect('pagPrincipal.html')  # Redirige a la página de usuario normal
    
def registro(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/accounts/login/")
    else:
        form = CustomUserCreationForm()

    return render(request, "registro.html", {"form": form})