from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name="index"),
    url(r'^curso\/?$', RedirectView.as_view(url='cursos', permanent=False), name='redirect_curso'),
    url(r'^cursos\/?$', views.CursoList.as_view(), name="curso_list"),
    url(r'^curso/(?P<slug>\S+)$', views.CursoDetalle.as_view(), name="curso_detalle"),
    url(r'^registrarse\/?$', views.Registrarse.as_view(), name="registrar"),
    url(r'^registrarse_post\/?$', views.RegistrarsePost, name="registrar_post"),
    url(r'^crear_cohorte\/?$', views.CrearCohorte, name="crear_cohorte"),
    url(r'^activar_lt\/?$', views.ActivarLT, name="activar_lt"),
    url(r'^mis_cursos\/?$', views.CursosLT.as_view(), name="mis_cursos"),
    url(r'^mis_notas/(?P<pk>\d+)$', views.MisNotas, name="mis_notas"),
    url(r'^actividad/(?P<pk>\d+)$', views.ActividadDetalle, name="actividad"),
    url(r'^certificados\/?$', views.Certificados, name="certificados"),
    url(r'^reportes\/?$', views.Reportes, name="reportes"),
    url(r'^reporte1\/?$', views.Reporte1, name="reporte1"),
    url(r'^reporte2\/?$', views.Reporte2, name="reporte2"),
    url(r'^reporte3\/?$', views.Reporte3, name="reporte3"),
    url(r'^reporte4\/?$', views.Reporte4, name="reporte4"),
    url(r'^reporte5\/?$', views.Reporte5, name="reporte5"),
    url(r'^reporte6\/?$', views.Reporte6, name="reporte6"),
    url(r'^reporte7\/?$', views.Reporte7, name="reporte7"),
    url(r'^reporte8\/?$', views.Reporte8, name="reporte8"),
    url(r'^reporte9\/?$', views.Reporte9, name="reporte9"),
    url(r'^mis_cursosmt\/?$', views.CursosMT.as_view(), name="mis_cursosmt"),
    url(r'^calificar\/?$', views.ProcesarCalificacion, name="calificar"),
    url(r'^calificar/(?P<pk>\d+)$', views.CalificarListaAct, name="calificar_lista"),
    url(r'^calificar/(?P<pk>\d+)/(?P<idact>\d+)$', views.CalificarActividad, name="calificar_actividad"),
)
