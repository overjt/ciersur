from django.urls import re_path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name="index"),
    re_path(r'^curso\/?$', RedirectView.as_view(url='cursos', permanent=False), name='redirect_curso'),
    re_path(r'^cursos\/?$', views.CursoList.as_view(), name="curso_list"),
    re_path(r'^curso/(?P<slug>\S+)$', views.CursoDetalle.as_view(), name="curso_detalle"),
    re_path(r'^registrarse\/?$', views.Registrarse.as_view(), name="registrar"),
    re_path(r'^registrarse_post\/?$', views.RegistrarsePost, name="registrar_post"),
    re_path(r'^crear_cohorte\/?$', views.CrearCohorte, name="crear_cohorte"),
    re_path(r'^activar_lt\/?$', views.ActivarLT, name="activar_lt"),
    re_path(r'^mis_cursos\/?$', views.CursosLT.as_view(), name="mis_cursos"),
    re_path(r'^mis_notas/(?P<pk>\d+)$', views.MisNotas, name="mis_notas"),
    re_path(r'^actividad/(?P<pk>\d+)$', views.ActividadDetalle, name="actividad"),
    re_path(r'^certificados\/?$', views.Certificados, name="certificados"),
    re_path(r'^reportes\/?$', views.Reportes, name="reportes"),
    re_path(r'^reporte1\/?$', views.Reporte1, name="reporte1"),
    re_path(r'^reporte2\/?$', views.Reporte2, name="reporte2"),
    re_path(r'^reporte3\/?$', views.Reporte3, name="reporte3"),
    re_path(r'^reporte4\/?$', views.Reporte4, name="reporte4"),
    re_path(r'^reporte5\/?$', views.Reporte5, name="reporte5"),
    re_path(r'^reporte6\/?$', views.Reporte6, name="reporte6"),
    re_path(r'^reporte7\/?$', views.Reporte7, name="reporte7"),
    re_path(r'^reporte8\/?$', views.Reporte8, name="reporte8"),
    re_path(r'^reporte9\/?$', views.Reporte9, name="reporte9"),
    re_path(r'^mis_cursosmt\/?$', views.CursosMT.as_view(), name="mis_cursosmt"),
    re_path(r'^calificar\/?$', views.ProcesarCalificacion, name="calificar"),
    re_path(r'^calificar/(?P<pk>\d+)$', views.CalificarListaAct, name="calificar_lista"),
    re_path(r'^calificar/(?P<pk>\d+)/(?P<idact>\d+)$', views.CalificarActividad, name="calificar_actividad"),
]
