from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy

from .models import *
from .forms import *

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

# Create your views here.
def home(request):
    return render(request, "aplicacion/home.html")

def cursos(request):
    contexto = {'cursos': Curso.objects.all()}
    return render(request, "aplicacion/cursos.html", contexto)



def estudiantes(request):
    return render(request, "aplicacion/estudiantes.html")

def entregables(request):
    return render(request, "aplicacion/entregables.html")

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

  

def buscar(request):
    return render(request, "aplicacion/buscar.html")

def buscarCursos(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        cursos = Curso.objects.filter(nombre__icontains=patron)
        contexto = {"cursos": cursos }
        return render(request, "aplicacion/cursos.html", contexto)
    return HttpResponse("No se ingresaron patrones de busqueda")

def deleteCurso(request, id_cursos):
    curso = Curso.objects.get(id=id_cursos)
    curso.delete()
    return redirect(reverse_lazy('cursos'))
#________________________________________________________ Profesores
def profesores(request):
    contexto = {'profesores': Profesor.objects.all()}
    return render(request, "aplicacion/profesores.html", contexto)

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

def deleteProfesor(request, id_profesor):
    profesor = Profesor.objects.get(id=id_profesor)
    profesor.delete()
    return redirect(reverse_lazy('profesores'))


#________________________________________________________ Estudiantes

class CustomLogoutView(LogoutView):
    # Permitir tanto GET como POST
    http_method_names = ['get', 'post']


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
                return render(request, "aplicacion/home.html", {"mensaje": f"Bienvenido {usuario}"})
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