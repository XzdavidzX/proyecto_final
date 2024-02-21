from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import *
from .forms import *

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DetailView
from django.views.generic import DeleteView

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "aplicacion/base.html")



def estudiantes(request):
    return render(request, "aplicacion/estudiantes.html")

def entregables(request):
    return render(request, "aplicacion/entregables.html")

@login_required
def cursos(request):
    ctx = {"cursos": Curso.objects.all() }
    return render(request, "aplicacion/cursos.html", ctx)

@login_required
def cursoForm(request):
    if request.method == "POST":                
        curso = Curso(nombre=request.POST['nombre'], comision=request.POST['comision'])
        curso.save()
        return HttpResponse("Se grabo con exito el curso!")
    
    return render(request, "aplicacion/cursoForm.html")

@login_required
def cursoForm2(request):
    if request.method == "POST":   
        miForm = CursoForm(request.POST)
        if miForm.is_valid():
            curso_nombre = miForm.cleaned_data.get('nombre')
            curso_comision = miForm.cleaned_data.get('comision')
            curso = Curso(nombre=curso_nombre, comision=curso_comision)
            curso.save()
            return render(request, "aplicacion/base.html")
    else:
        miForm = CursoForm()

    return render(request, "aplicacion/cursoForm2.html", {"form":miForm})

@login_required
def buscarComision(request):
    return render(request, "aplicacion/buscarComision.html")

@login_required
def buscar2(request):
    if request.GET['comision']:
        comision = request.GET['comision']
        cursos = Curso.objects.filter(comision__icontains=comision)
        return render(request, 
                      "aplicacion/resultadosComision.html", 
                      {"comision": comision, "cursos":cursos})
    return HttpResponse("No se ingresaron datos para buscar!")


#__________________________________
@login_required
def profesores(request):
    ctx = {'profesores': Profesor.objects.all() }
    return render(request, "aplicacion/profesores.html", ctx)

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
        miForm = ProfesorForm(initial={'nombre':profesor.nombre, 
                                       'apellido':profesor.apellido, 
                                       'email':profesor.email, 
                                       'profesion':profesor.profesion})         
    return render(request, "aplicacion/profesorForm.html", {'form': miForm})   

@login_required
def deleteProfesor(request, id_profesor):
    profesor = Profesor.objects.get(id=id_profesor)
    profesor.delete()
    return redirect(reverse_lazy('profesores'))

@login_required
def createProfesor(request):    
    if request.method == "POST":
        miForm = ProfesorForm(request.POST)
        if miForm.is_valid():
            p_nombre = miForm.cleaned_data.get('nombre')
            p_apellido = miForm.cleaned_data.get('apellido')
            p_email = miForm.cleaned_data.get('email')
            p_profesion = miForm.cleaned_data.get('profesion')
            profesor = Profesor(nombre=p_nombre, 
                             apellido=p_apellido,
                             email=p_email,
                             profesion=p_profesion,
                             )
            profesor.save()
            return redirect(reverse_lazy('profesores'))
    else:
        miForm = ProfesorForm()

    return render(request, "aplicacion/profesorForm.html", {"form":miForm})

#______ Class Based View

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

#____________ Login, Logout, Registracion
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
    #_____________________                
                try:
                    avatar = Avatar.objects.get(user=request.user.id).imagen.url
                except:
                    avatar = '/media/avatares/default.png'
                finally:
                    request.session['avatar'] = avatar

                return render(request, "aplicacion/base.html", {"mensaje": f"Bienvenido {usuario}"})
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
            return render(request, "aplicacion/base.html", {"mensaje":"Usuario Creado"})        
    else:
        form = RegistroUsuariosForm() # UserCreationForm 

    return render(request, "aplicacion/registro.html", {"form": form})   

#_________________ Registración de usuarios
# 

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
            return render(request, "aplicacion/base.html", {'mensaje': f"Usuario {usuario.username} actualizado correctamente"})
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
            u = User.objects.get(username=request.user)
            #_________________ Esto es para borrar el avatar anterior
            avatarViejo = Avatar.objects.filter(user=u)
            if len(avatarViejo) > 0: # Si esto es verdad quiere decir que hay un Avatar previo
                avatarViejo[0].delete()

            #_________________ Grabo avatar nuevo
            avatar = Avatar(user=u, imagen=form.cleaned_data['imagen'])
            avatar.save()

            #_________________ Almacenar en session la url del avatar para mostrarla en base
            imagen = Avatar.objects.get(user=request.user.id).imagen.url
            request.session['avatar'] = imagen

            return render(request, "aplicacion/base.html")
    else:
        form = AvatarFormulario()
    return render(request, "aplicacion/agregarAvatar.html", {'form': form})


