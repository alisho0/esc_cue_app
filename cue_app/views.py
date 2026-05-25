from django.shortcuts import render, redirect
from .models import Escuela, Alumno


def login_view(request):

    if request.method == "POST":

        cue = request.POST.get("cue")
        dni = request.POST.get("dni")

        try:
            escuela = Escuela.objects.get(
                cue=cue,
                dni=dni
            )

            request.session["escuela_id"] = escuela.id

            return redirect("dashboard")

        except Escuela.DoesNotExist:
            return render(request, "escuelas/login.html", {
                "error": "Credenciales inválidas"
            })

    return render(request, "escuelas/login.html")


def dashboard(request):

    escuela_id = request.session.get("escuela_id")

    if not escuela_id:
        return redirect("login")

    escuela = Escuela.objects.get(id=escuela_id)

    alumnos = Alumno.objects.filter(
        escuela=escuela
    )

    if request.method == "POST":

        for alumno in alumnos:
            valor = request.POST.get(f"cumple_{alumno.id}")
            alumno.cumple_asistencia = valor == "on"
            alumno.save()

        alumnos = Alumno.objects.filter(escuela=escuela)

    total_alumnos = alumnos.count()
    total_cumplen = alumnos.filter(cumple_asistencia=True).count()
    total_pendientes = total_alumnos - total_cumplen

    return render(request, "escuelas/dashboard.html", {
        "escuela": escuela,
        "alumnos": alumnos,
        "total_alumnos": total_alumnos,
        "total_cumplen": total_cumplen,
        "total_pendientes": total_pendientes,
    })


def logout_view(request):
    request.session.pop("escuela_id", None)
    return redirect("login")