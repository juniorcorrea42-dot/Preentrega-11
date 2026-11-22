from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm, PerfilForm
from .models import Perfil

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Perfil.objects.create(user=usuario)
            return redirect('login')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'accounts/registro.html', {'form': form})

@login_required
def perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(user=request.user)
    return render(request, 'accounts/perfil.html', {'perfil': perfil_usuario})

@login_required
def editar_perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil_usuario)

    return render(request, 'accounts/editar_perfil.html', {'form': form})


