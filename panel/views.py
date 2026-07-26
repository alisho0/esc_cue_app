from functools import wraps

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, resolve_url, get_object_or_404

from cue_app.forms import PanelAlumnoForm
from cue_app.models import Alumno, Escuela


def _sanitize_alumno_post_data(post_data):
    cleaned_data = post_data.copy()
    if 'cumple_asistencia' in cleaned_data:
        cleaned_data['cumple_asistencia'] = 'on' if cleaned_data.get('cumple_asistencia') == 'on' else False
    else:
        cleaned_data['cumple_asistencia'] = False
    return cleaned_data


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


@login_required
@admin_required
def escuelas(request):
    cue_query = request.GET.get('cue', '').strip()
    estado = request.GET.get('estado', 'todos')

    escuelas = Escuela.objects.all().order_by('nombre')

    if cue_query:
        escuelas = escuelas.filter(cue__icontains=cue_query)

    if estado == 'completada':
        escuelas = escuelas.filter(asistencia_completada=True)
    elif estado == 'pendiente':
        escuelas = escuelas.filter(asistencia_completada=False)

    context = {
        'escuelas': escuelas,
        'total_escuelas': escuelas.count(),
        'cue_query': cue_query,
        'estado': estado,
    }
    return render(request, 'admin_panel/escuelas.html', context)


@login_required
@admin_required
def alumnos(request):
    dni_query = request.GET.get('dni', '').strip()
    cue_query = request.GET.get('cue', '').strip()
    creado = request.GET.get('creado', 'todos')
    cumple = request.GET.get('cumple', 'todos')

    alumnos_qs = Alumno.objects.select_related('escuela').all().order_by('apellido', 'nombre')

    if dni_query:
        alumnos_qs = alumnos_qs.filter(dni__icontains=dni_query)

    if cue_query:
        alumnos_qs = alumnos_qs.filter(escuela__cue__icontains=cue_query)

    if creado == 'si':
        alumnos_qs = alumnos_qs.filter(creado_por_escuela=True)
    elif creado == 'no':
        alumnos_qs = alumnos_qs.filter(creado_por_escuela=False)

    if cumple == 'si':
        alumnos_qs = alumnos_qs.filter(cumple_asistencia=True)
    elif cumple == 'no':
        alumnos_qs = alumnos_qs.filter(cumple_asistencia=False)

    paginator = Paginator(alumnos_qs, 20)
    page_number = request.GET.get('page', 1)

    try:
        alumnos_page = paginator.page(page_number)
    except PageNotAnInteger:
        alumnos_page = paginator.page(1)
    except EmptyPage:
        alumnos_page = paginator.page(paginator.num_pages)

    query_data = request.GET.copy()
    if 'page' in query_data:
        del query_data['page']
    query_string = query_data.urlencode()

    context = {
        'alumnos': alumnos_page,
        'dni_query': dni_query,
        'cue_query': cue_query,
        'creado': creado,
        'cumple': cumple,
        'total_alumnos': alumnos_qs.count(),
        'paginator': paginator,
        'page_obj': alumnos_page,
        'query_string': query_string,
        'escuelas': Escuela.objects.order_by('nombre'),
    }
    return render(request, 'admin_panel/alumnos.html', context)


@login_required
@admin_required
def alumno_crear(request):
    if request.method != 'POST':
        return redirect('panel:alumnos')

    form = PanelAlumnoForm(_sanitize_alumno_post_data(request.POST))
    if form.is_valid():
        alumno = form.save(commit=False)
        alumno.creado_por_escuela = False
        alumno.editado_por_escuela = False
        alumno.save()

    return redirect('panel:alumnos')


@login_required
@admin_required
def alumno_editar(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    if request.method != 'POST':
        return redirect('panel:alumnos')

    form = PanelAlumnoForm(_sanitize_alumno_post_data(request.POST), instance=alumno)
    if form.is_valid():
        alumno = form.save()
        alumno.editado_por_escuela = True
        alumno.save(update_fields=['editado_por_escuela'])

    return redirect('panel:alumnos')


@login_required
@admin_required
def alumno_eliminar(request, alumno_id):
    if request.method == 'POST':
        alumno = get_object_or_404(Alumno, pk=alumno_id)
        alumno.delete()

    return redirect('panel:alumnos')
