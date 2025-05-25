import datetime # Added for fecha_inscripcion
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import *


class CrearNotaTest(TestCase):
    def setUp(self):
        '''
import datetime # Added for fecha_inscripcion
        Se crea el ambiente
        '''
        persona = Persona(cedula=333, nombre="Usuario LT Test", apellidos="", correo="admin@over.cf", celular=None, direccion=None, fecha_nacimiento="1993-11-13", sexo="M", departamento="VC", ciudad="") #Se crea una persona con cedula 333
        persona.save()
        usuariolt = get_user_model().objects.create_user(id_persona=persona.cedula, tipo='4', password='testpassword') #Se establece esa persona como LT
        usuariolt.save()

        curso = Curso(nombre="Matemáticas",descripcion="Descripción de Matematicas",slug="matematicas") #Se crea un curso
        curso.save()

        actividad = Actividad(id_curso=curso,nombre="Actividad 1",descripcion="Descripción actividad 1",porcentaje=35.0) #Se crea una actividad en ese curso
        actividad.save()

        cohorte = Cohorte(id_curso=curso,semestre="2015-1") # Se crea una cohorte en el curso
        cohorte.save()

        curso_lt = LT_Curso(id_lt=usuariolt,id_curso_cohorte=cohorte, fecha_inscripcion=datetime.date.today()) #Se establece una relación entre el docente LT y el curso
        curso_lt.save()

        self.usuariolt = usuariolt # Corrected variable name
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
        persona1 = Persona(cedula=111, nombre="Usuario test", apellidos="", correo="admin@over.cf", celular=None, direccion=None, fecha_nacimiento="1993-11-13", sexo="M", departamento="VC", ciudad="") #Se crea una persona con cedula 111
        persona1.save()
        # Use create_user for Usuario model as it handles password hashing and uses USERNAME_FIELD
        user1 = get_user_model().objects.create_user(id_persona=persona1.cedula, password="hola", tipo='1')
        # user1.save() # create_user already saves

        persona2 = Persona(cedula=333, nombre="Usuario test", apellidos="", correo="test2@over.cf", celular=None, direccion=None, fecha_nacimiento="1993-11-13", sexo="M", departamento="VC", ciudad="") #Se crea una persona con cedula 333
        persona2.save()
        user2 = get_user_model().objects.create_user(id_persona=persona2.cedula, password="hola2", tipo='1')
        # user2.save() # create_user already saves


    def testAuthNum(self):
        # USERNAME_FIELD for Usuario is 'id_persona', which refers to the Persona's cedula (PK).
        login1_success = self.client.login(username=111, password='hola') 
        self.assertTrue(login1_success)
        login2_success = self.client.login(username=333, password='hola2')
        self.assertTrue(login2_success)

    def test_auth_con_texto1(self):
        # cedula is IntegerField, so passing text will raise ValueError during query prep.
        self.assertRaises(ValueError, Persona.objects.get, cedula = "admin")
    def test_auth_con_texto2(self):
        self.assertRaises(ValueError, Persona.objects.get, cedula = "juan")
    def test_auth_con_texto3(self):
        self.assertRaises(ValueError, Persona.objects.get, cedula = "' or '1'='1")


