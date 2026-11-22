# Blog Django - Energías Renovables ♻️

Aplicación web de blog desarrollada con Django, orientada a la divulgación sobre transición energética y energías renovables. En esta versión (**Preentrega 11**), se incorporó un sistema de **autenticación, gestión de usuarios, perfiles con avatar y protección de rutas del CRUD**.

## 🚀 Cómo ejecutar el proyecto

1. **Clonar el repositorio y entrar al directorio:**
   ```bash
   git clone URL_DEL_REPOSITORIO
   cd blog_consola
   ```

2. **Crear y activar el entorno virtual:**
   * Windows (PowerShell):
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```
   * Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar migraciones y levantar el servidor:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
   Abrir en el navegador: `http://127.0.0.1:8000/`

---

## 🔐 Autenticación y Usuarios (App `accounts`)

Se creó la aplicación `accounts` (registrada en `INSTALLED_APPS`) para centralizar la lógica de usuarios y perfiles, configurando las redirecciones en `blog_project/settings.py`:
* `LOGIN_URL = 'login'`
* `LOGIN_REDIRECT_URL = 'lista_posts'`
* `LOGOUT_REDIRECT_URL = 'lista_posts'`

### Cómo funciona el registro
* Disponible en `/accounts/registro/`.
* Utiliza un formulario personalizado (`RegistroUsuarioForm` en `accounts/forms.py`) basado en `UserCreationForm`, sumando los campos `email`, `first_name` y `last_name`.
* Al enviarse por `POST`, la vista `accounts.views.registro` valida los datos, crea el usuario en la base de datos, genera automáticamente su `Perfil` asociado y redirige a `/accounts/login/`.

### Cómo iniciar sesión
* Disponible en `/accounts/login/`.
* Utiliza la vista nativa `LoginView` de `django.contrib.auth` con un template propio (`accounts/templates/accounts/login.html`) que hereda de `posts/base.html`.
* Al autenticarse correctamente, Django redirige al listado de publicaciones (`lista_posts`) y la barra de navegación cambia para mostrar **Mi perfil**, **Crear post**, el saludo al usuario y **Cerrar sesión**.

### Cómo cerrar sesión
* Disponible en `/accounts/logout/`.
* Utiliza la vista nativa `LogoutView`.
* El botón **Cerrar sesión** en `base.html` envía un formulario seguro por método `POST` con `{% csrf_token %}`. Al cerrar la sesión, el usuario es redirigido a `lista_posts` y el menú vuelve a mostrar **Iniciar sesión** y **Registrarse**.

---

## 👤 Modelo `Perfil` y Avatares

### Cómo se creó el modelo `Perfil`
En `accounts/models.py` se definió el modelo `Perfil` relacionado uno a uno con el modelo `User` de Django:
* `user`: `OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')`.
* `biografia`: `TextField` opcional.
* `link_web`: `URLField` opcional.
* `avatar`: `ImageField` opcional.

Se generaron y aplicaron las migraciones (`makemigrations` y `migrate`) y se registró el modelo en `accounts/admin.py` para administrarlo desde `/admin/`.

### Cómo se configuran los avatares de perfil
* El campo `avatar` usa `upload_to='avatares/'`, guardando las imágenes subidas en `media/avatares/`.
* En `blog_project/settings.py` se mantienen configurados `MEDIA_URL = '/media/'` y `MEDIA_ROOT = BASE_DIR / 'media'`.
* En `blog_project/urls.py` se sirven los archivos multimedia en desarrollo cuando `settings.DEBUG` está activo mediante `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`.
* El formulario de edición de perfil (`accounts/templates/accounts/editar_perfil.html`) incluye `enctype="multipart/form-data"` y la vista recibe `request.FILES`, apoyándose en la librería `Pillow`.

---

## 🛡️ Rutas protegidas y vistas que requieren autenticación

Las acciones sensibles del CRUD de publicaciones y la gestión del perfil están protegidas mediante el decorador `@login_required`. Si un usuario no autenticado intenta ingresar, Django lo redirige automáticamente a `/accounts/login/`.

| Ruta protegida | Vista que requiere autenticación | Función |
| :--- | :--- | :--- |
| `/posts/nuevo/` | `posts.views.crear_post` | Crear una nueva publicación |
| `/posts/<int:pk>/editar/` | `posts.views.editar_post` | Editar una publicación existente |
| `/posts/<int:pk>/eliminar/` | `posts.views.eliminar_post` | Eliminar una publicación |
| `/accounts/perfil/` | `accounts.views.perfil` | Ver el perfil del usuario autenticado |
| `/accounts/perfil/editar/` | `accounts.views.editar_perfil` | Editar biografía, link y avatar |

El listado (`/posts/`) y el detalle de publicaciones (`/posts/<int:pk>/`) siguen siendo públicos, pero los botones de creación, edición y eliminación solo se muestran si `user.is_authenticated` es verdadero.