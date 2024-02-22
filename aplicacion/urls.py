from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('cursos/', cursos, name="cursos"),   
    path('curso_form/', cursoForm, name="cursoForm"),
    path('curso_borrar/<id_cursos>/', deleteCurso, name="cursoBorrar"),

    #____________________________________________________ Profesores
    path('profesores/', profesores, name="profesores"),
    path('profesor_crear/', createProfesor, name="profesorCrear"),
    path('profesor_borrar/<id_profesor>/', deleteProfesor, name="profesorBorrar"),
    #____________________________________________________ Estudiantes
    path('estudiantes/', EstudianteList.as_view(), name="estudiantes"),
    path('estudiante_create/', EstudianteCreate.as_view(), name="estudiante_create"),
    path('estudiante_update/<int:pk>/', EstudianteUpdate.as_view(), name="estudiante_update"),
    path('estudiante_delete/<int:pk>/', EstudianteDelete.as_view(), name="estudiante_delete"),


    path('buscar/', buscar, name="buscar"),
    path('buscarCursos/', buscarCursos, name="buscarCursos"),
]