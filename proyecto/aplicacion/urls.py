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

    path('login/', login_request, name="login"),
    path('logout/', CustomLogoutView.as_view(template_name="aplicacion/logout.html"), name="logout"),
    path('register/', register, name="register"),
    path('eliminar_usuario/', eliminarUsuario, name='eliminar_usuario'),
    path('confirmar_eliminar/', delete_user, name="confirmar_eliminar"),

    path('buscar/', buscar, name="buscar"),
    path('buscarCursos/', buscarCursos, name="buscarCursos"),

    path('editar_perfil/', editarPerfil, name="editar_perfil"),
    path('agregar_avatar/', agregarAvatar, name="agregar_avatar"),

]