from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField
from .models import *


class CursoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'slug',
        'descripcion'
    )
    prepopulated_fields = {'slug': ('nombre',)}
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}

class ActividadAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'descripcion',
        'porcentaje'
    )
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}


class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        'cedula',
        'nombre',
        'apellidos',
        'correo',
        'fecha_nacimiento'
    )

class CursoLTAdmin(admin.ModelAdmin):
    list_display = (
        'id_lt',
        'id_curso_cohorte',
        'fecha_inscripcion',
        'aprobado'
    )

class NotaAdmin(admin.ModelAdmin):
    list_display = (
        'id_lt_curso',
        'id_actividad',
        'calificacion'
    )

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('id_persona', 'tipo')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('id_persona', 'password', 'tipo', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id_persona', 'tipo', 'is_admin')
    list_filter = ('is_admin','tipo')
    fieldsets = (
        (None, {'fields': ('id_persona', 'password')}),
        ('Permissions', {'fields': ('is_admin','tipo')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id_persona', 'tipo', 'password1', 'password2')}
        ),
    )
    search_fields = ('id_persona',)
    ordering = ('id_persona',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(Usuario, MyUserAdmin)
admin.site.register(Persona,PersonaAdmin)
admin.site.register(Historial_Academico)
admin.site.register(Historial_Laboral)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Actividad, ActividadAdmin)
admin.site.register(Cohorte)
admin.site.register(Posible_LT)
admin.site.register(LT_Curso,CursoLTAdmin)
admin.site.register(MT_Curso)
admin.site.register(Nota,NotaAdmin)
admin.site.register(Certificado)
admin.site.unregister(Group)
