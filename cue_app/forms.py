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
        fields = ['nombre', 'apellido', 'dni', 'curso', 'localidad', 'fecha_nacimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}),
            'curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Curso'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Localidad'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }


class PanelAlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['escuela', 'nombre', 'apellido', 'dni', 'curso', 'localidad', 'fecha_nacimiento', 'cumple_asistencia']
        widgets = {
            'escuela': forms.Select(attrs={'class': 'rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 w-full'}),
            'nombre': forms.TextInput(attrs={'class': 'rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 w-full', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 w-full', 'placeholder': 'Apellido'}),
            'dni': forms.TextInput(attrs={'class': 'rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 w-full', 'placeholder': 'DNI'}),
            'curso': forms.TextInput(attrs={'class': 'rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 w-full', 'placeholder': 'Curso'}),
            'localidad': forms.TextInput(attrs={'class': 'rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 w-full', 'placeholder': 'Localidad'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 w-full', 'type': 'date'}, format='%Y-%m-%d'),
            'cumple_asistencia': forms.CheckboxInput(attrs={'class': 'h-5 w-5 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500'}),
        }


class CursoEditForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['curso']
        widgets = {
            'curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Curso'}),
        }