from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

# Vistas de páginas informativas
def inicio(request):
    return render(request, "posts/inicio.html")

def acerca(request):
    return render(request, "posts/acerca.html")

def contacto(request):
    return render(request, "posts/contacto.html")


# 1. LISTAR POSTS (Read)
def lista_posts(request):
    # Mostramos todos los posts ordenados del más reciente al más antiguo
    posts = Post.objects.all().order_by("-fecha_creacion")
    return render(request, "posts/lista_posts.html", {"posts": posts})


# 2. DETALLE DE UN POST (Read)
def detalle_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/detalle_post.html", {"post": post})

# Vistas protegidas del CRUD
# 3. CREAR UN POST (Create)
@login_required
def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect("detalle_post", pk=post.pk)
    else:
        form = PostForm()

    return render(request, "posts/post_form.html", {
        "form": form,
        "titulo_pagina": "Crear nuevo post",
        "texto_boton": "Crear"
    })


# 4. EDITAR UN POST (Update)
@login_required
def editar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("detalle_post", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "posts/post_form.html", {
        "form": form,
        "post": post,
        "titulo_pagina": "Editar post",
        "texto_boton": "Guardar cambios"
    })


# 5. BORRAR UN POST (Delete)
@login_required
def eliminar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect("lista_posts")

    return render(request, "posts/post_confirm_delete.html", {"post": post})