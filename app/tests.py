from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import *


class CrearNotaTest(TestCase):
    def setUp(self):
        '''
        Se crea el ambiente
        '''
        persona = Persona(333,"Usuario LT Test","","admin@over.cf","1993-11-13","M","VC","") #Se crea una persona con cedula 333
        persona.save()
        usuariolt = get_user_model().objects.create(id_persona=persona, tipo=4) #Se establece esa persona como LT
        usuariolt.save()

        curso = Curso(nombre="Matemáticas",descripcion="Descripción de Matematicas",slug="matematicas") #Se crea un curso
        curso.save()

        actividad = Actividad(id_curso=curso,nombre="Actividad 1",descripcion="Descripción actividad 1",porcentaje=35) #Se crea una actividad en ese curso
        actividad.save()

        cohorte = Cohorte(id_curso=curso,semestre="2015-1") # Se crea una cohorte en el curso
        cohorte.save()

        curso_lt = LT_Curso(id_lt=usuariolt,id_curso_cohorte=cohorte) #Se establece una relación entre el docente LT y el curso
        curso_lt.save()

        self.personaLT = usuariolt
        self.curso_lt  = curso_lt
        self.actividad = actividad

    def test_limites_nota(self):
        nota = Nota(id_lt_curso=self.curso_lt, id_actividad=self.actividad, calificacion=None)
        nota.set_calificacion(0) #Valor en el límite inferior
        self.assertEqual(nota.calificacion, 0) #Se comprueba si la calificación es igual a 0
        self.assertRaises(IndexError,  nota.set_calificacion,-1) #Se verifica si el Valor por debajo del límite de la función levanta la excepción IndexError
        nota.set_calificacion(3) #Valor válido
        self.assertEqual(nota.calificacion, 3) #Se comprueba si la calificación es igual a 3
        nota.set_calificacion(5) #Valor en el limite superior
        self.assertEqual(nota.calificacion, 5) #Se comprueba si la calificación es igual a 3
        self.assertRaises(IndexError, nota.set_calificacion, 6) #Se comprueba si Valor por encima del límite de la función levanta la excepción IndexError
        

class CedulaAuthTest(TestCase):
    def setUp(self):
        persona = Persona(111,"Usuario test","","admin@over.cf","1993-11-13","M","VC","") #Se crea una persona con cedula 111
        persona.save()
        user = get_user_model().objects.create(id_persona=persona, password="hola", tipo=1) #Se crea un usuario con cedula 111 y password hola
        user.save()
        persona = Persona(333,"Usuario test","","test2@over.cf","1993-11-13","M","VC","") #Se crea una persona con cedula 333 
        persona.save()
        user = get_user_model().objects.create(id_persona=persona, password="hola2", tipo=1) #Se crea un usuario con cedula 333 y password hola
        user.save()

    def testAuthNum(self):
        self.client.login(id_persona=Persona.objects.get(cedula = 111), password='hola') #Se comprueba si existe un login con la cedula numerica 111
        self.client.login(id_persona=Persona.objects.get(cedula = 333), password='hola2') #Se comprueba si existe un login con la cedula numerica 111
    def test_auth_con_texto1(self):
        self.client.login(id_persona=Persona.objects.get(cedula = "admin"), password='hola2')#Se comprueba si existe un login con la cedula admin
    def test_auth_con_texto2(self):
        self.client.login(id_persona=Persona.objects.get(cedula = "juan"), password='hola2') #Se comprueba si existe un login con la cedula juan
    def test_auth_con_texto3(self):
        self.client.login(id_persona=Persona.objects.get(cedula = "' or '1'='1"), password='hola2') #Se comprueba si existe un login con la cedula ' or '1'='1


