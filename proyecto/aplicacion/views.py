from django.shortcuts import render, redirect
from django.http      import HttpResponse
from django.urls      import reverse_lazy

from .models import *
from .forms  import *

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DetailView
from django.views.generic import DeleteView

from django.contrib.auth.forms      import AuthenticationForm
from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views      import LogoutView
from django.shortcuts               import render, redirect
from .forms                         import AvatarFormulario
from .models                        import Avatar

# Create your views here.
def home(request):
    return render(request, "aplicacion/home.html")

def cursos(request):
    contexto = {'cursos': Curso.objects.all()}
    return render(request, "aplicacion/cursos.html", contexto)



def estudiantes(request):
    return render(request, "aplicacion/estudiantes.html")

@login_required
def cursoForm(request):
    if request.method == "POST":
        miForm = CursoForm(request.POST)
        if miForm.is_valid():
            curso_nombre = miForm.cleaned_data.get("nombre")
            curso_comision = miForm.cleaned_data.get("comision")
            curso = Curso(nombre=curso_nombre, comision=curso_comision)
            curso.save()
            return render(request, "aplicacion/home.html")

    else:    
        miForm = CursoForm()

    return render(request, "aplicacion/cursoForm.html", {"form": miForm })

  
@login_required
def buscar(request):
    return render(request, "aplicacion/buscar.html")  

@login_required
def buscarCursos(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        cursos = Curso.objects.filter(nombre__icontains=patron)
        contexto = {"cursos": cursos }
        return render(request, "aplicacion/cursos.html", contexto)
    return HttpResponse("No se ingresaron patrones de busqueda")

@login_required
def deleteCurso(request, id_cursos):
    curso = Curso.objects.get(id=id_cursos)
    curso.delete()
    return redirect(reverse_lazy('cursos'))
#________________________________________________________ Profesores
@login_required
def profesores(request):
    contexto = {'profesores': Profesor.objects.all()}
    return render(request, "aplicacion/profesores.html", contexto)

@login_required
def createProfesor(request):
    if request.method == "POST":
        miForm = ProfesorForm(request.POST)
        if miForm.is_valid():
            prof_nombre = miForm.cleaned_data.get("nombre")
            prof_apellido = miForm.cleaned_data.get("apellido")
            prof_email = miForm.cleaned_data.get("email")
            prof_profesion = miForm.cleaned_data.get("profesion")
            profesor = Profesor(nombre=prof_nombre, apellido=prof_apellido,
                                email=prof_email, profesion=prof_profesion)
            profesor.save()
            return redirect(reverse_lazy('profesores'))

    else:    
        miForm = ProfesorForm()

    return render(request, "aplicacion/profesorForm.html", {"form": miForm })  

@login_required
def updateProfesor(request, id_profesor):
    profesor = Profesor.objects.get(id=id_profesor)
    if request.method == "POST":
        miForm = ProfesorForm(request.POST)
        if miForm.is_valid():
            profesor.nombre = miForm.cleaned_data.get('nombre')
            profesor.apellido = miForm.cleaned_data.get('apellido')
            profesor.email = miForm.cleaned_data.get('email')
            profesor.profesion = miForm.cleaned_data.get('profesion') 
            profesor.save()
            return redirect(reverse_lazy('profesores'))   
    else:
        miForm = ProfesorForm(initial={
            'nombre': profesor.nombre,
            'apellido': profesor.apellido,
            'email': profesor.email,
            'profesion': profesor.profesion,
        })
    return render(request, "aplicacion/profesorForm.html", {'form': miForm})

@login_required
def deleteProfesor(request, id_profesor):
    profesor = Profesor.objects.get(id=id_profesor)
    profesor.delete()
    return redirect(reverse_lazy('profesores'))


#________________________________________________________ Estudiantes

class CustomLogoutView(LogoutView):
    # Permitir tanto GET como POST
    http_method_names = ['get', 'post']
    next_page = '/aplicacion/logout/'  # Página a la que se redirigirá después de cerrar sesión


class EstudianteList(LoginRequiredMixin, ListView):
    model = Estudiante

class EstudianteCreate(LoginRequiredMixin, CreateView):
    model = Estudiante
    fields = ['nombre', 'apellido', 'email']
    success_url = reverse_lazy('estudiantes')

class EstudianteDetail(LoginRequiredMixin, DetailView):
    model = Estudiante

class EstudianteUpdate(LoginRequiredMixin, UpdateView):
    model = Estudiante
    fields = ['nombre', 'apellido', 'email']
    success_url = reverse_lazy('estudiantes')    

class EstudianteDelete(LoginRequiredMixin, DeleteView):
    model = Estudiante
    success_url = reverse_lazy('estudiantes')    

#____________ Login, Logout, Registracion, delete
# 

def login_request(request):
    if request.method == "POST":
        miForm = AuthenticationForm(request, data=request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get('username')
            clave = miForm.cleaned_data.get('password')
            user = authenticate(username=usuario, password=clave)
            if user is not None:
                login(request, user)               
                try:
                    avatar = Avatar.objects.get(user=request.user.id).imagen.url
                except:
                    avatar = '/media/avatares/default.png'
                finally:
                    request.session['avatar'] = avatar
                    return render(request, "aplicacion/home.html")
            else:
                return render(request, "aplicacion/login.html", {"form":miForm, "mensaje": "Datos Inválidos"})
        else:    
            return render(request, "aplicacion/login.html", {"form":miForm, "mensaje": "Datos Inválidos"})

    miForm = AuthenticationForm()

    return render(request, "aplicacion/login.html", {"form":miForm})    

def register(request):
    if request.method == 'POST':
        form = RegistroUsuariosForm(request.POST) # UserCreationForm 
        if form.is_valid():  # Si pasó la validación de Django
            usuario = form.cleaned_data.get('username')
            form.save()
            return render(request, "aplicacion/home.html", {"mensaje":"Usuario Creado"})        
    else:
        form = RegistroUsuariosForm() # UserCreationForm 

    return render(request, "aplicacion/registro.html", {"form": form})

def eliminarUsuario(request):
    return render(request, "aplicacion/eliminar_usuario.html")


@login_required
def delete_user(request):
    user = request.user
    try:
        user.delete()
    except User.DoesNotExist:
        print("El usuario no existe.")

    # Redirigir al usuario a la página principal después de eliminar su cuenta y cerrar sesión
    return redirect('home')





#_____________________________________________________editar perfil,avatar
@login_required
def editarPerfil(request):
    usuario = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            usuario.email = form.cleaned_data.get('email')
            usuario.password1 = form.cleaned_data.get('password1')
            usuario.password2 = form.cleaned_data.get('password2')
            usuario.first_name = form.cleaned_data.get('first_name')
            usuario.last_name = form.cleaned_data.get('last_name')
            usuario.save()
            return render(request, "aplicacion/home.html", {'mensaje': f"Usuario {usuario.username} actualizado correctamente"})
        else:
            return render(request, "aplicacion/editarPerfil.html", {'form': form})
    else:
        form = UserEditForm(instance=usuario)
    return render(request, "aplicacion/editarPerfil.html", {'form': form, 'usuario':usuario.username})



@login_required
def agregarAvatar(request):
    if request.method == "POST":
        form = AvatarFormulario(request.POST, request.FILES)
        if form.is_valid():
            usuario = request.user
            avatar_nuevo = form.cleaned_data['imagen']

            # Borrar el avatar anterior si existe
            Avatar.objects.filter(user=usuario).delete()

            # Grabar el nuevo avatar
            avatar = Avatar(user=usuario, imagen=avatar_nuevo)
            avatar.save()

            # Almacenar la URL del nuevo avatar en la sesión
            request.session["avatar"] = avatar.imagen.url

            return redirect("/aplicacion/")  # Redireccionar a la página principal
    else:
        form = AvatarFormulario()
    return render(request, "aplicacion/agregarAvatar.html", {'form': form})


