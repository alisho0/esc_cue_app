from functools import wraps

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, resolve_url

from cue_app.models import Alumno, Escuela


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = resolve_url(settings.LOGIN_URL)
            next_url = request.get_full_path()
            return redirect(f"{login_url}?next={next_url}")

        if not (request.user.is_staff or request.user.is_superuser):
            return HttpResponseForbidden("No tiene permisos para acceder a este panel.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


@login_required
@admin_required
def dashboard(request):
    total_escuelas = Escuela.objects.count()
    total_alumnos = Alumno.objects.count()
    escuelas_finalizadas = Escuela.objects.filter(asistencia_completada=True).count()
    escuelas_pendientes = Escuela.objects.filter(asistencia_completada=False).count()

    context = {
        'total_escuelas': total_escuelas,
        'total_alumnos': total_alumnos,
        'escuelas_finalizadas': escuelas_finalizadas,
        'escuelas_pendientes': escuelas_pendientes,
    }

    return render(request, 'admin_panel/dashboard.html', context)
