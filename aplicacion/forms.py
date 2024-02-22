from django import forms   

class CursoForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    comision = forms.IntegerField(required=True)


class ProfesorForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    apellido = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True, label="Cuenta de Correo")
    profesion = forms.CharField(max_length=50, required=True)