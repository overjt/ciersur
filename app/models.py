# -*- coding:Utf-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator


class CierUserManager(BaseUserManager):
    def create_user(self, id_persona, tipo, 
                    password=None):
        if not tipo:
            raise ValueError('Users must have a type')
        persona = Persona.objects.get(cedula=id_persona)
        user = self.model(id_persona=persona,tipo=tipo)
        user.set_password(password)
        return user

    def create_superuser(self, id_persona, tipo,
                         password):
        user = self.create_user(id_persona, tipo, 
                                password=password)
        user.tipo = 1
        user.is_admin = True
        user.save()
        return user


class Persona(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    correo = models.CharField(max_length=200, unique=True)
    celular = models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=200, null=True)
    fecha_nacimiento = models.DateField()
    SEXOS = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    sexo = models.CharField(max_length=1,choices=SEXOS)
    DEPS = (
        ('A', 'Amazonas'),
        ('Caq', 'Caquetá'),
        ('Ca', 'Cauca'),
        ('H', 'Huila'),
        ('N', 'Nariño'),
        ('P', 'Putumayo'),
        ('T', 'Tolima'),
        ('VC', 'Valle del Cauca'),
    )
    departamento = models.CharField(max_length=3,choices=DEPS)
    ciudad = models.CharField(max_length=15)

    def __str__(self):
        return "%s" % (self.cedula)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

class Usuario(AbstractBaseUser):
    id_persona = models.OneToOneField(Persona, verbose_name="Cédula de la persona")
    TIPOS = (
        ('1', 'Administrador'),
        ('2', 'Secretaria'),
        ('3', 'Master Teacher'),
        ('4', 'Leader Teacher')
    )
    tipo = models.CharField(max_length=1,choices=TIPOS)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CierUserManager()
    USERNAME_FIELD = 'id_persona'
    REQUIRED_FIELDS = ['tipo']


    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.id_persona.nombre, self.id_persona.apellidos)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.id_persona.nombre

    def get_tipo(self):
        return self.tipo

    def __str__(self):
        return "%s" % (self.id_persona)

    def has_perm(self, perm, obj=None):
        # Por definir los permisos
        return True

    def has_module_perms(self, app_label):
        # Por definir los permisos de los modulos
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Historial_Academico(models.Model):
    id_docente = models.ForeignKey(Persona, verbose_name="Cédula del docente")
    promocion = models.CharField(max_length=15)
    titulo = models.CharField(max_length=50)
    institucion = models.CharField(max_length=50)

    class Meta:
        unique_together = (("id_docente", "promocion","titulo","institucion"),)

    def __str__(self):
        return "%s - %s - %s. %s" % (self.id_docente, self.promocion, self.titulo, self.institucion)

    class Meta:
        verbose_name = "Historial Académico"
        verbose_name_plural = "Historiales Académicos"

class Historial_Laboral(models.Model):
    id_docente = models.ForeignKey(Persona,verbose_name="Cédula del docente")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    institucion = models.CharField(max_length=50)

    class Meta:
        unique_together = (("id_docente", "fecha_inicio","fecha_fin","institucion"),)

    def __str__(self):
        return "%s - (%s)-(%s). %s" % (str(self.id_docente),str(self.fecha_inicio), str(self.fecha_fin), self.institucion)

    class Meta:
        verbose_name = "Historial Laboral"
        verbose_name_plural = "Historiales Laborales"

class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("curso_detalle", kwargs={"slug": self.slug})
        
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

class Actividad(models.Model):
    id_curso = models.ForeignKey(Curso,verbose_name="Curso")
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=1000)
    porcentaje = models.FloatField()

    class Meta:
        unique_together = (("id_curso", "nombre"),)

    def __str__(self):
        return "%s - %s" % (str(self.id_curso), self.nombre)

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"

class Cohorte(models.Model):
    id_curso = models.ForeignKey(Curso,verbose_name="Curso")
    semestre = models.CharField(max_length=50)

    def __str__(self):
        return "%s - %s-%s" % (str(self.id_curso), self.semestre, str(self.id))


class Posible_LT(models.Model):
    id_docente = models.ForeignKey(Persona,verbose_name="Cédula del docente")
    id_curso = models.ForeignKey(Curso,verbose_name="Curso")

    class Meta:
        unique_together = (("id_docente", "id_curso"),)

    def __str__(self):
        return "%s - %s" % (str(self.id_docente), str(self.id_curso))

    class Meta:
        verbose_name = "Posible LT"
        verbose_name_plural = "Posibles LT"


class LT_Curso(models.Model):
    id_lt = models.ForeignKey(Usuario,verbose_name="Cédula del docente")
    id_curso_cohorte = models.ForeignKey(Cohorte,verbose_name="Curso - Cohorte")
    fecha_inscripcion = models.DateField()
    aprobado =  models.NullBooleanField(default=None)
    class Meta:
        unique_together = (("id_lt", "id_curso_cohorte"),)

    def __str__(self):
        return "%s - %s" % (str(self.id_lt),str(self.id_curso_cohorte))

    def get_curso(self):
        return self.id_curso_cohorte.id_curso

    class Meta:
        verbose_name = "Curso-LT"
        verbose_name_plural = "Cursos-LT"


class MT_Curso(models.Model):
    id_mt = models.ForeignKey(Usuario,verbose_name="Cédula del docente")
    id_curso_cohorte = models.ForeignKey(Cohorte,verbose_name="Curso - Cohorte")

    class Meta:
        unique_together = (("id_mt", "id_curso_cohorte"),)

    def __str__(self):
        return "%s - %s" % (str(self.id_mt),str(self.id_curso_cohorte))


    class Meta:
        verbose_name = "Curso-MT"
        verbose_name_plural = "Cursos-MT"


class Nota(models.Model):
    id_lt_curso = models.ForeignKey(LT_Curso, verbose_name="LT-Curso")
    id_actividad = models.ForeignKey(Actividad,verbose_name="Actividad")
    calificacion = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = (("id_lt_curso", "id_actividad"),)

    def __str__(self):
        return "%s - %s - %s" % (str(self.id_lt_curso),str(self.id_actividad), str(self.calificacion))

    def set_calificacion(self,nota):
        if not (nota >= 0 and nota <=  5):
            raise IndexError('The note must be between 0 and 5')
        else:
            self.calificacion = nota

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"        

class Certificado(models.Model):
    id_lt_curso = models.OneToOneField(LT_Curso, verbose_name="LT-Curso",primary_key=True)
    TIPOS = (
        ('A', 'Asistencia'),
        ('P', 'Participación'),
        ('E', 'Excelencia'),
    )
    tipo = models.CharField(max_length=1, choices=TIPOS)

    def __str__(self):
        return "%s - %s" % (str(self.id_lt_curso),str(self.tipo))

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"



