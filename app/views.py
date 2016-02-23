from django.views import generic
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
import weasyprint
from django.utils import timezone
from . import models
from . import forms

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'title': 'Centro de Innovación Educativa Regional CIER-SUR',
        'nbar': 'inicio'
    })
    return HttpResponse(template.render(context))

def Reportes(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))

    template = loader.get_template('reportes/reportes.html')
    context = RequestContext(request, {
        'title': 'Reportes - CIER-SUR',
        'nbar': 'panel'
    })
    return HttpResponse(template.render(context))

#Número de docentes estudiantes que han llegado en el mes de cada departamento
def Reporte1(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))


    if request.method == 'POST':
        form = forms.Reporte1(request.POST)
        if form.is_valid():
            mes = form.cleaned_data["mes"]
            anio = form.cleaned_data["anio"]
            estudiantes = models.LT_Curso.objects.all().filter(fecha_inscripcion__year=anio, fecha_inscripcion__month=mes)
            contador = {}
            for lt in estudiantes:
                departamento = lt.id_lt.id_persona.get_departamento_display()
                if departamento in contador:
                    contador[departamento] = contador[departamento] + 1
                else:
                    contador[departamento] = 1
            template = loader.get_template('reportes/reporte1.html')
            context = RequestContext(request, {
                'title': 'Número de docentes estudiantes que han llegado en el mes de cada departamento - CIER-SUR',
                'nbar': 'panel',
                'fecha': mes + '/' + anio,
                'object_list': contador,
            })
            return HttpResponse(template.render(context))
        else:
            form = forms.Reporte1()
            return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: # LTs que han llegado en el mes de cada departamento', 'action': '/reporte1', 'submit_text': 'Ver'})
    else:
        form = forms.Reporte1()
        return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: # LTs que han llegado en el mes de cada departamento', 'action': '/reporte1', 'submit_text': 'Ver'})

def Reporte2(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))


    if request.method == 'POST':
        form = forms.Reporte1(request.POST)
        if form.is_valid():
            mes = form.cleaned_data["mes"]
            anio = form.cleaned_data["anio"]
            estudiantes = models.LT_Curso.objects.all().filter(fecha_inscripcion__year=anio, fecha_inscripcion__month=mes)
            contador = {}
            for lt in estudiantes:
                curso = lt.id_curso_cohorte.id_curso.nombre
                if curso in contador:
                    contador[curso] = contador[curso] + 1
                else:
                    contador[curso] = 1
            sorted_list = [(k,v) for v,k in sorted(
                 [(v,k) for k,v in contador.items()]
                 )
            ]
            sorted_list.reverse()
            template = loader.get_template('reportes/reporte2.html')
            context = RequestContext(request, {
                'title': 'Cursos con mayor número de asistentes en el mes (Top 10) - CIER-SUR',
                'nbar': 'panel',
                'fecha': mes + '/' + anio,
                'object_list': sorted_list
            })
            return HttpResponse(template.render(context))
        else:
            form = forms.Reporte1()
            return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Cursos con mayor número de asistentes en el mes (Top 10)', 'action': '/reporte2', 'submit_text': 'Ver'})
    else:
        form = forms.Reporte1()
        return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Cursos con mayor número de asistentes en el mes (Top 10)', 'action': '/reporte2', 'submit_text': 'Ver'})

def Reporte3(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))
    ltcurso = models.LT_Curso.objects.all().exclude(aprobado=None)
    
    contadorReprobados = {}
    contadorAprobados = {}
    contadorPorcentaje = {}
    for lt in ltcurso:
        curso = lt.id_curso_cohorte.id_curso.nombre
        if not curso in contadorReprobados:
            contadorReprobados[curso] = 0

        if not curso in contadorAprobados:
            contadorAprobados[curso] = 0

        if lt.aprobado == True:
            contadorAprobados[curso] = contadorAprobados[curso] + 1
        else:
            contadorReprobados[curso] = contadorReprobados[curso] + 1
    
    for value in contadorAprobados:
        total = (contadorAprobados[value] + contadorReprobados[value])
        if total == 0:
            porcentajeReprobados = 0
        else:
            porcentajeReprobados = (contadorReprobados[value] * 100)/total

        if porcentajeReprobados >= 50:
            contadorPorcentaje[value] = porcentajeReprobados


    sorted_list = [(k,v) for v,k in sorted(
                 [(v,k) for k,v in contadorPorcentaje.items()]
                 )
            ]
    template = loader.get_template('reportes/reporte3.html')
    context = RequestContext(request, {
        'title': 'Cursos con menos potencial de avance - CIER-SUR',
        'nbar': 'panel',
        'object_list': sorted_list
    })
    return HttpResponse(template.render(context))


def Reporte4(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))


    if request.method == 'POST':
        form = forms.Reporte4(request.POST)
        if form.is_valid():
            semestre = form.cleaned_data["semestre"]
            cursos_semestre = models.Cohorte.objects.all().filter(semestre=semestre)
            estudiantes = models.LT_Curso.objects.all().filter(id_curso_cohorte=cursos_semestre)
            contadorReprobados = {}
            contadorAprobados = {}
            contadorPorcentaje = {}
            for lt in estudiantes:
                departamento = lt.id_lt.id_persona.get_departamento_display()
                print (departamento)
                if not departamento in contadorAprobados:
                    contadorAprobados[departamento] = 0
                if not departamento in contadorReprobados:
                    contadorReprobados[departamento] = 0

                if lt.aprobado == True:
                    contadorAprobados[departamento] = contadorAprobados[departamento] + 1
                else:
                    contadorReprobados[departamento] = contadorReprobados[departamento] + 1

            
            for value in contadorAprobados:
                total = contadorAprobados[value] + contadorReprobados[value]
                if total == 0:
                    contadorPorcentaje[value] = 0
                else:
                    contadorPorcentaje[value] = (contadorAprobados[value] * 100)/total

            template = loader.get_template('reportes/reporte4.html')
            context = RequestContext(request, {
                'title': 'Porcentaje de estudiantes que aprobaron los cursos de un semestre por departamento - CIER-SUR',
                'nbar': 'panel',
                'semestre': dict(form.fields['semestre'].choices)[semestre],
                'object_list': contadorPorcentaje,
            })
            return HttpResponse(template.render(context))
        else:
            form = forms.Reporte4()
            return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Porcentaje de estudiantes que aprobaron los cursos de un semestre por departamento', 'action': '/reporte4', 'submit_text': 'Ver'})
    else:
        form = forms.Reporte4()
        return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Porcentaje de estudiantes que aprobaron los cursos de un semestre por departamento', 'action': '/reporte4', 'submit_text': 'Ver'})

def Reporte5(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))


    if request.method == 'POST':
        form = forms.Reporte4(request.POST)
        if form.is_valid():
            semestre = form.cleaned_data["semestre"]
            cursos_semestre = models.Cohorte.objects.all().filter(semestre=semestre)
            estudiantes = models.LT_Curso.objects.all().filter(id_curso_cohorte=cursos_semestre)
            contadorReprobados = {}
            contadorAprobados = {}
            contadorPorcentaje = {}
            for lt in estudiantes:
                departamento = lt.id_lt.id_persona.get_departamento_display()
                print (departamento)
                if not departamento in contadorAprobados:
                    contadorAprobados[departamento] = 0
                if not departamento in contadorReprobados:
                    contadorReprobados[departamento] = 0

                if lt.aprobado == True:
                    contadorAprobados[departamento] = contadorAprobados[departamento] + 1
                else:
                    contadorReprobados[departamento] = contadorReprobados[departamento] + 1

            
            for value in contadorAprobados:
                total = contadorAprobados[value] + contadorReprobados[value]
                if total == 0:
                    contadorPorcentaje[value] = 0
                else:
                    contadorPorcentaje[value] = (contadorReprobados[value] * 100)/total

            template = loader.get_template('reportes/reporte5.html')
            context = RequestContext(request, {
                'title': 'Porcentaje de estudiantes que reprobaron los cursos de un semestre por departamento - CIER-SUR',
                'nbar': 'panel',
                'semestre': dict(form.fields['semestre'].choices)[semestre],
                'object_list': contadorPorcentaje,
            })
            return HttpResponse(template.render(context))
        else:
            form = forms.Reporte4()
            return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Porcentaje de estudiantes que reprobaron los cursos de un semestre por departamento', 'action': '/reporte5', 'submit_text': 'Ver'})
    else:
        form = forms.Reporte4()
        return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Porcentaje de estudiantes que reprobaron los cursos de un semestre por departamento', 'action': '/reporte5', 'submit_text': 'Ver'})



def Reporte6(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))


    if request.method == 'POST':
        form = forms.Reporte6(request.POST)
        if form.is_valid():
            estudiante = form.cleaned_data["id_lt_curso"]
            template = loader.get_template('reportes/reporte6.html')
            objects = models.Nota.objects.all().filter(id_lt_curso=estudiante)

            context = RequestContext(request, {
                'title': 'Detalle del reporte de notas por estudiante - CIER-SUR',
                'nbar': 'panel',
                'object_list': objects,
                'estudiante': estudiante.id_lt.get_full_name(),
                'curso': estudiante.id_curso_cohorte.id_curso.nombre
            })
            return HttpResponse(template.render(context))
        else:
            form = forms.Reporte6()
            return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Detalle del reporte de notas por estudiante', 'action': '/reporte6', 'submit_text': 'Ver'})
    else:
        form = forms.Reporte6()
        return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Detalle del reporte de notas por estudiante', 'action': '/reporte6', 'submit_text': 'Ver'})



def Reporte7(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))
    ltcurso = models.LT_Curso.objects.all().exclude(aprobado=None).exclude(aprobado=False)
    template = loader.get_template('reportes/reporte7.html')
    context = RequestContext(request, {
        'title': 'Histórico de estudiantes que hayan ganado un curso - CIER-SUR',
        'nbar': 'panel',
        'object_list': ltcurso
    })
    return HttpResponse(template.render(context))

def Reporte8(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))


    if request.method == 'POST':
        form = forms.Reporte8(request.POST)
        if form.is_valid():
            curso = form.cleaned_data["id_curso"]
            curso_cohortes = models.Cohorte.objects.all().filter(id_curso=curso)
            estudiantes = models.LT_Curso.objects.all().filter(id_curso_cohorte=curso_cohortes)

            template = loader.get_template('reportes/reporte8.html')
            context = RequestContext(request, {
                'title': 'Detalle de estudiantes en un curso por departamentos - CIER-SUR',
                'nbar': 'panel',
                'curso': curso.nombre,
                'object_list': estudiantes,
            })
            return HttpResponse(template.render(context))
        else:
            form = forms.Reporte8()
            return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Detalle de estudiantes en un curso por departamentos', 'action': '/reporte8', 'submit_text': 'Ver'})
    else:
        form = forms.Reporte8()
        return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Detalle de estudiantes en un curso por departamentos', 'action': '/reporte8', 'submit_text': 'Ver'})

def Reporte9(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))


    if request.method == 'POST':
        form = forms.Reporte4(request.POST)
        if form.is_valid():
            semestre = form.cleaned_data["semestre"]
            cursos_semestre = models.Cohorte.objects.all().filter(semestre=semestre)
            estudiantes = models.LT_Curso.objects.all().filter(id_curso_cohorte=cursos_semestre)
            contadorReprobados = {}
            contadorAprobados = {}
            contadorPorcentaje = {}
            for lt in estudiantes:
                departamento = lt.id_lt.id_persona.get_departamento_display()
                print (departamento)
                if not departamento in contadorAprobados:
                    contadorAprobados[departamento] = 0
                if not departamento in contadorReprobados:
                    contadorReprobados[departamento] = 0

                if lt.aprobado == True:
                    contadorAprobados[departamento] = contadorAprobados[departamento] + 1
                else:
                    contadorReprobados[departamento] = contadorReprobados[departamento] + 1

            deps = []
            lista_aprobados = []
            lista_reprobados = []
            for value in contadorAprobados:
                total = contadorAprobados[value] + contadorReprobados[value]
                temp_aprobado = (contadorAprobados[value] * 100)/total
                temp_reprobado = (contadorReprobados[value] * 100)/total
                deps.append(value)
                lista_aprobados.append(temp_aprobado)
                lista_reprobados.append(temp_reprobado)



            template = loader.get_template('reportes/reporte9.html')
            context = RequestContext(request, {
                'title': 'Porcentaje de estudiantes que aprobaron los cursos de un semestre por departamento - CIER-SUR',
                'nbar': 'panel',
                'semestre': dict(form.fields['semestre'].choices)[semestre],
                'lista_deps': deps,
                'lista_aprobados': lista_aprobados,
                'lista_reprobados': lista_reprobados
            })
            return HttpResponse(template.render(context))
        else:
            form = forms.Reporte4()
            return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Porcentaje de estudiantes que aprobaron los cursos de un semestre por departamento', 'action': '/reporte9', 'submit_text': 'Ver'})
    else:
        form = forms.Reporte4()
        return render(request, 'form.html', {'form': form, 'titulo_form': 'Reporte: Porcentaje de estudiantes que aprobaron los cursos de un semestre por departamento', 'action': '/reporte9', 'submit_text': 'Ver'})


def ActivarLT(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))


    if request.method == 'POST':
        form = forms.ActivarLT(request.POST)
        if form.is_valid():
            id_posiblelt = form.cleaned_data["id_posibleLT"]
            curso = id_posiblelt.id_curso
            cohorte = form.cleaned_data["cohorte"]
            if cohorte.id_curso != curso:
                context = RequestContext(request, {
                    'title': 'Activar LT - CIER-SUR',
                    'nbar': 'panel',
                    'titulo_mensaje': 'Error al activar un LT',
                    'mensaje': 'La cohorte seleccionada no concuerda con el curso',
                })
                return HttpResponse(template.render(context))
            try:
                usuario = models.Usuario.objects.get(id_persona=id_posiblelt.id_docente)
            except models.Usuario.DoesNotExist:
                usuario = models.Usuario.objects.create_user(id_persona=id_posiblelt.id_docente.cedula, tipo=4, password="demo")
                usuario.save()
            curso_lt = models.LT_Curso(id_lt=usuario, id_curso_cohorte=cohorte, fecha_inscripcion=timezone.now())
            curso_lt.save()
            id_posiblelt.delete()
            context = RequestContext(request, {
                'title': 'Activar LT - CIER-SUR',
                'nbar': 'panel',
                'titulo_mensaje': 'LT Activo',
                'mensaje': 'El LT se activó con éxito',
            })
            return HttpResponse(template.render(context))           

        else:
            form = forms.ActivarLT()
            return render(request, 'form.html', {'form': form, 'titulo_form': 'Activar LT', 'action': '/activar_lt', 'submit_text': 'Activar'})
    else:
        form = forms.ActivarLT()
        return render(request, 'form.html', {'form': form, 'titulo_form': 'Activar LT', 'action': '/activar_lt', 'submit_text': 'Activar'})



def CrearCohorte(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '2' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))


    if request.method == 'POST':
        form = forms.RegistroCohorteForm(request.POST)
        if form.is_valid():
            semestre = form.cleaned_data["semestre"]
            curso = form.cleaned_data["id_curso"]
            cursos_semetres = models.Cohorte.objects.all().filter(id_curso=curso,semestre=semestre)
            if cursos_semetres.count() >= 10:
                context = RequestContext(request, {
                    'title': 'Cohorte - CIER-SUR',
                    'nbar': 'panel',
                    'titulo_mensaje': 'Error al crear la cohorte',
                    'mensaje': 'El curso seleccionado tiene el máximo de cohortes por semestre (10)',
                })
                return HttpResponse(template.render(context))
            else:
                cohorte = models.Cohorte(id_curso=curso,semestre=semestre)
                cohorte.save()
                context = RequestContext(request, {
                    'title': 'Cohorte - CIER-SUR',
                    'nbar': 'panel',
                    'titulo_mensaje': 'Cohorte creada',
                    'mensaje': 'Se ha creado una cohorte para el curso seleccionado',
                })
                return HttpResponse(template.render(context))
        else:
            form = forms.RegistroCohorteForm()
            return render(request, 'form.html', {'form': form, 'titulo_form': 'Crear Cohorte', 'action': '/crear_cohorte', 'submit_text': 'Crear'})
    else:
        form = forms.RegistroCohorteForm()
        return render(request, 'form.html', {'form': form, 'titulo_form': 'Crear Cohorte', 'action': '/crear_cohorte', 'submit_text': 'Crear'})


def RegistrarsePost(request):
    if request.method == 'POST':
        template = loader.get_template('mensaje.html')
        form = forms.RegistroForm(request.POST)
        print(form.non_field_errors())
        if form.is_valid():
            curso_solicitado = None
            try: #Comprueba si el curso existe
                curso_solicitado = models.Curso.objects.get(id=form.cleaned_data["curso"])
            except models.Curso.DoesNotExist:
                context = RequestContext(request, {
                            'title': 'Registro - CIER-SUR',
                            'nbar': 'registrar',
                            'titulo_mensaje': 'Error al registrarse',
                            'mensaje': 'No existe el curso solicitado ',
                    })
                return HttpResponse(template.render(context))
            if request.user.is_authenticated():
                if str(form.cleaned_data["id_documento"]) == str(request.user.id_persona):
                    try:
                        persona = models.Persona.objects.get(cedula=form.cleaned_data["id_documento"])
                        posible_lt = models.Posible_LT.objects.all().filter(id_docente=persona)
                        for p_lt in posible_lt:
                            if p_lt.id_curso == curso_solicitado:                                
                                context = RequestContext(request, {
                                    'title': 'Registro - CIER-SUR',
                                    'nbar': 'registrar',
                                    'titulo_mensaje': 'Error al registrarse',
                                    'mensaje': 'Ya existe una solicitud pendiente para este curso.',
                                })
                                return HttpResponse(template.render(context))
                        posible_lt = models.Posible_LT(id_docente=persona,id_curso=curso_solicitado)
                        posible_lt.save()
                        context = RequestContext(request, {
                            'title': 'Registro - CIER-SUR',
                            'nbar': 'registrar',
                            'titulo_mensaje': 'Registro Exitoso',
                            'mensaje': 'EL registro se ha realizado con éxito',
                        })
                        return HttpResponse(template.render(context))
                    except models.Persona.DoesNotExist:
                        context = RequestContext(request, {
                            'title': 'Registro - CIER-SUR',
                            'nbar': 'registrar',
                            'titulo_mensaje': 'Error al registrarse',
                            'mensaje': 'Tu cuenta al parecer no existe',
                        })
                        return HttpResponse(template.render(context))
                    except models.Posible_LT.DoesNotExist:
                        posible_lt = models.Posible_LT(id_docente=persona,id_curso=curso_solicitado)
                        posible_lt.save()
                        context = RequestContext(request, {
                            'title': 'Registro - CIER-SUR',
                            'nbar': 'registrar',
                            'titulo_mensaje': 'Registro Exitoso',
                            'mensaje': 'EL registro se ha realizado con éxito',
                        })
                        return HttpResponse(template.render(context))
                else:
                    context = RequestContext(request, {
                        'title': 'Registro - CIER-SUR',
                        'nbar': 'registrar',
                        'titulo_mensaje': 'Error al registrarse',
                        'mensaje': 'El documento de identificación no corresponde al documento de la sesión activa',
                    })
                    return HttpResponse(template.render(context))
            else:
                try:
                    persona = models.Persona.objects.get(cedula=form.cleaned_data["id_documento"])
                    posible_lt = models.Posible_LT.objects.all().filter(id_docente=persona)
                    for p_lt in posible_lt:
                        if p_lt.id_curso == curso_solicitado:                                
                            context = RequestContext(request, {
                                'title': 'Registro - CIER-SUR',
                                'nbar': 'registrar',
                                'titulo_mensaje': 'Error al registrarse',
                                'mensaje': 'Ya existe una solicitud pendiente para este curso.',
                            })
                            return HttpResponse(template.render(context))
                    posible_lt = models.Posible_LT(id_docente=persona,id_curso=curso_solicitado)
                    posible_lt.save()
                    context = RequestContext(request, {
                        'title': 'Registro - CIER-SUR',
                        'nbar': 'registrar',
                        'titulo_mensaje': 'Registro Exitoso',
                        'mensaje': 'EL registro se ha realizado con éxito',
                    })
                    return HttpResponse(template.render(context))
                except models.Persona.DoesNotExist:
                    persona = models.Persona(form.cleaned_data["id_documento"],form.cleaned_data["nombre"],form.cleaned_data["apellidos"],form.cleaned_data["correo"],form.cleaned_data["celular"],form.cleaned_data["direccion"],"1950-11-13",form.cleaned_data["sexo"],form.cleaned_data["departamento"],form.cleaned_data["ciudad"]) #Se crea una persona con cedula 333
                    persona.save()
                    posible_lt = models.Posible_LT(id_docente=persona,id_curso=curso_solicitado)
                    posible_lt.save()
                    context = RequestContext(request, {
                        'title': 'Registro - CIER-SUR',
                        'nbar': 'registrar',
                        'titulo_mensaje': 'Registro Exitoso',
                        'mensaje': 'EL registro se ha realizado con éxito',
                    })
                    return HttpResponse(template.render(context))
                except models.Posible_LT.DoesNotExist:
                    posible_lt = models.Posible_LT(id_docente=persona,id_curso=curso_solicitado)
                    posible_lt.save()
                    context = RequestContext(request, {
                        'title': 'Registro - CIER-SUR',
                        'nbar': 'registrar',
                        'titulo_mensaje': 'Registro Exitoso',
                        'mensaje': 'EL registro se ha realizado con éxito',
                    })
                    return HttpResponse(template.render(context))
        else:
            context = RequestContext(request, {
                'title': 'Registro - CIER-SUR',
                'nbar': 'registrar',
                'titulo_mensaje': 'Error al registrar',
                'mensaje': 'El formulario no es válido por favor revisa los datos cuidadosamente.',
            })
            return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/registrarse')


class Registrarse(generic.ListView):

    queryset = models.Curso.objects.all()
    template_name = "registration/registro.html"

    def get_context_data(self, **kwargs):
        context = super(Registrarse, self).get_context_data(**kwargs)
        context['title'] = "Registrarse - CIER-SUR"
        context['nbar'] = "registrar"
        return context

class CursoList(generic.ListView):

    queryset = models.Curso.objects.all()
    template_name = "cursos.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CursoList, self).get_context_data(**kwargs)
        context['title'] = "Cursos disponibles - CIER-SUR"
        context['nbar'] = "curso_list"
        return context

class CursoDetalle(generic.DetailView):
    model = models.Curso
    template_name = "curso.html"

    def get_context_data(self, **kwargs):
        context = super(CursoDetalle, self).get_context_data(**kwargs)
        context['title'] = kwargs['object'].nombre + " - CIER-SUR"
        context['nbar'] = "curso_list"
        return context

def ActividadDetalle(request, pk):
    if request.method == "GET":
        template = loader.get_template('mensaje.html')
        if not request.user.is_authenticated() or (request.user.get_tipo() == '2'):
            context = RequestContext(request, {
                    'title': '404 - CIER-SUR',
                    'nbar': 'index',
                    'titulo_mensaje': 'Error 404',
                    'mensaje': 'Página no encontrada',
            })
            return HttpResponse(template.render(context))
        act = models.Actividad.objects.get(id=pk)
        template = loader.get_template('actividad.html')
        context = RequestContext(request, {
            'title': 'Actividad - CIER-SUR',
            'nbar': 'inicio',
            'object': act,
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/')

def CalificarListaAct(request, pk):
    if request.method == "GET":
        template = loader.get_template('mensaje.html')
        if not request.user.is_authenticated() or (request.user.get_tipo() != '3' and request.user.get_tipo() != '1'):
            context = RequestContext(request, {
                    'title': '404 - CIER-SUR',
                    'nbar': 'index',
                    'titulo_mensaje': 'Error 404',
                    'mensaje': 'Página no encontrada',
            })
            return HttpResponse(template.render(context))

        cohorte = models.Cohorte.objects.get(id=pk)
        actividades = models.Actividad.objects.all().filter(id_curso=cohorte.id_curso)
        template = loader.get_template('listActCalificar.html')
        context = RequestContext(request, {
                'title': 'Lista de actividades -CIER-SUR',
                'nbar': 'panel',
                'curso': cohorte.id_curso.nombre,
                'id_cohorte': pk,
                'object_list': actividades,
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/')

def CalificarActividad(request, pk, idact):
    if request.method == "GET":
        template = loader.get_template('mensaje.html')
        if not request.user.is_authenticated() or (request.user.get_tipo() != '3' and request.user.get_tipo() != '1'):
            context = RequestContext(request, {
                    'title': '404 - CIER-SUR',
                    'nbar': 'index',
                    'titulo_mensaje': 'Error 404',
                    'mensaje': 'Página no encontrada',
            })
            return HttpResponse(template.render(context))

        cohorte = models.Cohorte.objects.get(id=pk)
        actividad = models.Actividad.objects.get(id=idact)
        estudiantes = models.LT_Curso.objects.all().filter(id_curso_cohorte=cohorte)
        template = loader.get_template('calificarActividad.html')
        context = RequestContext(request, {
                'title': 'Lista de actividades -CIER-SUR',
                'nbar': 'panel',
                'curso': cohorte.id_curso.nombre,
                'actividad': actividad,
                'cohorte': cohorte.id,
                'estudiantes': estudiantes,
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/')

def ProcesarCalificacion(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated() or (request.user.get_tipo() != '3' and request.user.get_tipo() != '1'):
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))

    if request.method == 'POST':
        actividad = models.Actividad.objects.get(id=request.POST.get('actividad'))
        cohorte = models.Cohorte.objects.get(id=request.POST.get('cohorte'))
        estudiantes = models.LT_Curso.objects.all().filter(id_curso_cohorte=cohorte)
        for estudiante in estudiantes:
            calificacion = request.POST.get('est'+str(estudiante.id))
            try:
                nota = models.Nota.objects.get(id_lt_curso=estudiante,id_actividad=actividad)
                nota.calificacion = calificacion
                nota.save()
            except models.Nota.DoesNotExist:                
                nota = models.Nota(id_lt_curso=estudiante,id_actividad=actividad,calificacion=calificacion)
                nota.save()

            actividades = models.Actividad.objects.all().filter(id_curso=cohorte.id_curso)
            notas = models.Nota.objects.all().filter(id_lt_curso=estudiante)
            if len(notas) == len(actividades):
                notafinal = 0
                for nota in notas:
                    notafinal = notafinal + nota.calificacion
                notafinal = notafinal / len(notas)
                porcentajeNota = notafinal*100/5

                if porcentajeNota >= 71:
                    tipo = 'E'
                elif porcentajeNota >= 51 and porcentajeNota <= 70:
                    tipo = 'P'
                elif porcentajeNota > 0 and porcentajeNota <= 50:
                    tipo = 'A'
                else:
                    tipo = None

                if tipo == None:
                    estudiante.aprobado = False
                    estudiante.save()
                    try:
                        certificado = models.Certificado.objects.get(id_lt_curso=estudiante)
                        certificado.delete()
                    except models.Certificado.DoesNotExist:
                        print ("ok")
                else:
                    estudiante.aprobado = True
                    estudiante.save()
                    try:
                        certificado = models.Certificado.objects.get(id_lt_curso=estudiante)
                        certificado.tipo = tipo
                        certificado.save()
                    except models.Certificado.DoesNotExist:
                        certificado = models.Certificado(id_lt_curso=estudiante,tipo=tipo)
                        certificado.save()

        context = RequestContext(request, {
                'title': 'Calificar - CIER-SUR',
                'nbar': 'panel',
                'titulo_mensaje': 'Actividad calificada',
                'mensaje': 'La actividad ' + actividad.nombre + ' del curso ' + cohorte.id_curso.nombre + ' fue calificada',
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/')



def MisNotas(request, pk):
    if request.method == "GET":
        template = loader.get_template('mensaje.html')
        if not request.user.is_authenticated() or (request.user.get_tipo() != '4' and request.user.get_tipo() != '1'):
            context = RequestContext(request, {
                    'title': '404 - CIER-SUR',
                    'nbar': 'index',
                    'titulo_mensaje': 'Error 404',
                    'mensaje': 'Página no encontrada',
            })
            return HttpResponse(template.render(context))
        objects = models.Nota.objects.all().filter(id_lt_curso=models.LT_Curso.objects.get(id=pk))
        template = loader.get_template('misnotas.html')
        context = RequestContext(request, {
            'title': 'Mis notas - CIER-SUR',
            'nbar': 'inicio',
            'object_list': objects,
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/')

class CursosLT(generic.ListView):
    template_name = "cursosLT.html"

    def get_queryset(self):
        return models.LT_Curso.objects.all().filter(id_lt=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CursosLT, self).get_context_data(**kwargs)
        context['title'] = "Mis Cursos - CIER-SUR"
        context['nbar'] = "panel"
        return context

class CursosMT(generic.ListView):
    template_name = "cursosMT.html"

    def get_queryset(self):
        tipo = self.request.user.get_tipo()
        if tipo == '1':
            return models.MT_Curso.objects.all()
        else:
            return models.MT_Curso.objects.all().filter(id_mt=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CursosMT, self).get_context_data(**kwargs)
        context['title'] = "Mis Cursos - CIER-SUR"
        context['nbar'] = "panel"
        return context


def Certificados(request):
    template = loader.get_template('mensaje.html')
    if not request.user.is_authenticated():
        context = RequestContext(request, {
                'title': '404 - CIER-SUR',
                'nbar': 'index',
                'titulo_mensaje': 'Error 404',
                'mensaje': 'Página no encontrada',
        })
        return HttpResponse(template.render(context))

    if request.method == 'POST':
        ltcurso = models.LT_Curso.objects.get(id=request.POST.get("ltcurso"))
        if ltcurso.aprobado == None:
            context = RequestContext(request, {
                'title': 'Certificado - CIER-SUR',
                'nbar': 'panel',
                'titulo_mensaje': 'Error. El estudiante no ha terminado el curso',
                'mensaje': 'El estudiante identificado con la cédula ' + str(ltcurso.id_lt.id_persona.cedula) + ', no ha finalizado el curso de ' + ltcurso.id_curso_cohorte.id_curso.nombre,
            })
            return HttpResponse(template.render(context))
        elif ltcurso.aprobado == False:
            context = RequestContext(request, {
                'title': 'Certificado - CIER-SUR',
                'nbar': 'panel',
                'titulo_mensaje': 'Error. El estudiante reprobó el curso',
                'mensaje': 'El estudiante identificado con la cédula ' + str(ltcurso.id_lt.id_persona.cedula) + ', REPROBÓ el curso de ' + ltcurso.id_curso_cohorte.id_curso.nombre,
            })
            return HttpResponse(template.render(context))
        else:                      
            try:                
                certificado = models.Certificado.objects.get(id_lt_curso=ltcurso)
                template = loader.get_template("certificado/plantillacertificado.html")
                context = RequestContext(request, {
                    'nombre': ltcurso.id_lt.get_full_name(),
                    'cedula': ltcurso.id_lt.id_persona.cedula,
                    'tipo': certificado.get_tipo_display(),
                    'curso': ltcurso.id_curso_cohorte.id_curso.nombre
                })
                html = template.render(context)
                response = HttpResponse(content_type="application/pdf")
                weasyprint.HTML(string=html).write_pdf(response)
                return response
            except models.Certificado.DoesNotExist:
                context = RequestContext(request, {
                    'title': 'Certificado - CIER-SUR',
                    'nbar': 'panel',
                    'titulo_mensaje': 'Error al descargar el certificado',
                    'mensaje': 'Un error ocurrió el descargar el certificado, por favor escriba un mensaje al administrador',
                })
                return HttpResponse(template.render(context))
    else:
        tipo = request.user.get_tipo()
        if tipo == '1' or tipo == '2':
            lista = models.LT_Curso.objects.all()
        elif tipo == '3':
            lista = models.LT_Curso.objects.all() #TODO
        else:
            lista = models.LT_Curso.objects.all().filter(id_lt=request.user)

        template = loader.get_template('escogerCertificado.html')
        certificadosList = models.Certificado.objects.all().filter()
        context = RequestContext(request, {
                'title': 'Certificado - CIER-SUR',
                'nbar': 'panel',
                'object_list': lista
        })
        return HttpResponse(template.render(context))


