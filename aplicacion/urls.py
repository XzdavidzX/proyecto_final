from django.urls import path, include
from .views import *

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name="inicio"),

    path('cursos/', cursos, name="cursos"),
    path('entregables/', entregables, name="entregables"),

    path('curso_form/', cursoForm, name="curso_form"),
    path('curso_form2/', cursoForm2, name="curso_form2"),

    path('buscar_comision/', buscarComision, name="buscar_comision"),
    path('buscar2/', buscar2, name="buscar2"),
#_______________________
    path('profesores/', profesores, name="profesores"),
    path('update_profesor/<id_profesor>/', updateProfesor, name="update_profesor"),
    path('delete_profesor/<id_profesor>/', deleteProfesor, name="delete_profesor"),
    path('create_profesor/', createProfesor, name="create_profesor"),

    path('estudiantes/', EstudianteList.as_view(), name="estudiantes"),
    path('create_estudiante/', EstudianteCreate.as_view(), name="create_estudiante"),
    path('detail_estudiante/<int:pk>/', EstudianteDetail.as_view(), name="detail_estudiante"),
    path('update_estudiante/<int:pk>/', EstudianteUpdate.as_view(), name="update_estudiante"),
    path('delete_estudiante/<int:pk>/', EstudianteDelete.as_view(), name="delete_estudiante"),

    path('login/', login_request, name="login"),
    path('logout/', LogoutView.as_view(template_name="aplicacion/logout.html"), name="logout"),
    path('register/', register, name="register"),

    path('editar_perfil/', editarPerfil, name="editar_perfil"),
    path('agregar_avatar/', agregarAvatar, name="agregar_avatar"),
]
