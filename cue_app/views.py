from django.http import HttpResponse

from .exports import generar_excel_global, generar_excel_escuela
from .models import Escuela, Alumno
from .forms import AlumnoForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    error = None

    if request.method == "POST":

        cue = request.POST.get('cue')
        dni = request.POST.get('dni')

        try:
            escuela = Escuela.objects.get(cue=cue)
            
            if escuela.dni == dni:
                login(request, escuela.user)
                return redirect('dashboard')
            else:
                error = "DNI incorrecto"
        except Escuela.DoesNotExist:
            error = "CUE no encontrado"

    return render(
        request,
        'escuelas/login.html',
        {'error': error}
    )

@login_required
def finalizar_carga(request):
    escuela = request.user.escuela
    escuela.asistencia_completada = True
    escuela.save()

    return redirect('dashboard') 

@login_required
def dashboard(request):

    if request.user.is_staff:
        return redirect('/admin')

    escuela = Escuela.objects.get(
        user=request.user
    )

    alumnos = Alumno.objects.filter(
        escuela=escuela
    )

    if request.method == "POST":

        for alumno in alumnos:

            valor = request.POST.get(
                f'cumple_{alumno.id}'
            )

            alumno.cumple_asistencia = valor == 'on'
            alumno.save()

        return redirect('dashboard')

    total_alumnos = alumnos.count()
    total_cumplen = alumnos.filter(cumple_asistencia=True).count()
    total_pendientes = alumnos.filter(cumple_asistencia=False).count()

    return render(
        request,
        'escuelas/dashboard.html',
        {
            'escuela': escuela,
            'alumnos': alumnos,
            'total_alumnos': total_alumnos,
            'total_cumplen': total_cumplen,
            'total_pendientes': total_pendientes
        }
    )


def logout_view(request):

    logout(request)

    return redirect('login')


@login_required
def exportar_excel(request):

    if not request.user.is_staff:
        return redirect('dashboard')

    wb = generar_excel_global()

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename="alumnos.xlsx"'

    wb.save(response)

    return response


@login_required
def exportar_escuela(request, escuela_id):

    if not request.user.is_staff:
        return redirect('dashboard')

    wb = generar_excel_escuela(escuela_id)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = f'attachment; filename="escuela_{escuela_id}.xlsx"'

    wb.save(response)

    return response


@login_required
def agregar_alumno(request):

    if request.user.is_staff:
        return redirect('/admin')

    escuela = Escuela.objects.get(
        user=request.user
    )

    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.escuela = escuela
            alumno.creado_por_escuela = True
            alumno.save()
            return redirect('dashboard')
    else:
        form = AlumnoForm()

    return render(
        request,
        'escuelas/agregar_alumno.html',
        {'form': form, 'escuela': escuela}
    )
