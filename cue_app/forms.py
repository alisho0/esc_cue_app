from django import forms
from .models import Alumno


class LoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'dni', 'curso', 'localidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}),
            'curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Curso'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Localidad'}),
        }