from django import forms
from . import models

class RegistroCohorteForm(forms.ModelForm):
    class Meta:
        model = models.Cohorte
        fields = ['id_curso']

    SEMESTRES = (
        ('15a', '2015A'),
        ('15b', '2015B'),
        ('16a', '2016A'),
        ('16b', '2016B'),
        ('17a', '2017A'),
        ('17b', '2017B'),
        ('18a', '2018A'),
        ('18b', '2018B'),
    )
    semestre = forms.ChoiceField(widget=forms.Select,label='semestre',choices=SEMESTRES) 

class ActivarLT(forms.Form):
    id_posibleLT = forms.ModelChoiceField(widget=forms.Select,label="Solicitud",queryset=models.Posible_LT.objects.all())
    cohorte = forms.ModelChoiceField(widget=forms.Select,label="Cohorte",queryset=models.Cohorte.objects.all())


class CertificadoForm(forms.ModelForm):
    class Meta:
        model = models.Certificado
        fields = ['id_lt_curso']

class RegistroForm(forms.Form):
    nombre = forms.CharField(label='nombre')
    apellidos = forms.CharField(label='apellidos')
    id_documento = forms.IntegerField(label='id_documento')
    SEXOS = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    sexo = forms.ChoiceField(label='sexo',widget=forms.RadioSelect, choices=SEXOS)
    correo = forms.EmailField(label='correo')
    celular = forms.CharField(label='celular')
    direccion = forms.CharField(label='direccion')
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
    departamento = forms.ChoiceField(widget=forms.Select,label='departamento',choices=DEPS)
    curso = forms.IntegerField(label='curso')
    ciudad = forms.CharField(label='ciudad')

#Número de docentes estudiantes que han llegado en el mes de cada departamento
class Reporte1(forms.Form):
    MESES = (
        ('01', 'Enero'),
        ('02', 'Febrero'),
        ('03', 'Marzo'),
        ('04', 'Abril'),
        ('05', 'Mayo'),
        ('06', 'Junio'),
        ('07', 'Julio'),
        ('08', 'Agosto'),
        ('09', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre'),
    )
    ANIOS = (
        ('2015', '2015'),
        ('2016', '2016'),
        ('2017', '2017'),
        ('2018', '2018'),
    )
    mes = forms.ChoiceField(widget=forms.Select,label='Mes',choices=MESES)
    anio = forms.ChoiceField(widget=forms.Select,label='Año',choices=ANIOS)

class Reporte4(forms.Form):
    SEMESTRES = (
        ('15a', '2015A'),
        ('15b', '2015B'),
        ('16a', '2016A'),
        ('16b', '2016B'),
        ('17a', '2017A'),
        ('17b', '2017B'),
        ('18a', '2018A'),
        ('18b', '2018B'),
    )
    semestre = forms.ChoiceField(widget=forms.Select,label='semestre',choices=SEMESTRES) 


class Reporte6(forms.ModelForm):
    class Meta:
        model = models.Nota
        fields = ['id_lt_curso']

class Reporte8(forms.ModelForm):
    class Meta:
        model = models.Cohorte
        fields = ['id_curso']