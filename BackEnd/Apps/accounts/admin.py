from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# @JavicSoftCode
from .models import SuperUser, User, UserAdmin


# Configuración del admin para SuperUser
class SuperUsuario(BaseUserAdmin):
  list_display = ('email_icon', 'username', 'first_name', 'last_name', 'birth_day', 'is_active', 'change_password_link')
  list_filter = ('is_staff', 'is_superuser', 'is_active')
  search_fields = ('email', 'username', 'first_name', 'last_name')
  ordering = ('email', 'username')
  readonly_fields = ('last_login', 'date_joined', 'password')

  # Formulario para actualizar un SuperUser
  fieldsets = (
    (_('Registro Super Usuario'),
     {'fields': ('email', 'username', 'password', 'is_active', 'is_staff', 'is_superuser')}),
    (_('Información Personal'), {'fields': ('first_name', 'last_name', 'birth_day')}),
    (_('Fechas Importantes'), {'fields': ('last_login', 'date_joined')}),
    (_('Permisos'), {'fields': ('groups', 'user_permissions')}),
  )

  # Formulario para un nuevo SuperUser
  add_fieldsets = (
    (_('Registrando Nuevo Super Usuario'), {'classes': ('wide',), 'fields': (
      'email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'), }),
    (_('Información Personal'), {'fields': ('first_name', 'last_name', 'birth_day')}),
    (_('Fechas Importantes'), {'fields': ('last_login', 'date_joined')}),
    (_('Permisos'), {'fields': ('groups', 'user_permissions')}),

  )

  class Media:
    css = {
      'all': ('css/adminDjango.css',)
    }

  def get_form(self, request, obj=None, **kwargs):
    """
          Agregacion de texto de ayuda, de acuerdo si se esta editando o creando un registro.
    """
    form = super(SuperUsuario, self).get_form(request, obj, **kwargs)
    if obj:  # Si estamos editando un usuario existente
      form.base_fields['is_staff'].help_text = (
        "Actualmente tiene acceso, al panel de Administrador."
      )
    else:
      form.base_fields['is_staff'].help_text = (
        "Tendra acceso al panel de Administrador."
      )
      form.base_fields['password1'].help_text = (
        "Cantraseña valida mayor a 8 caracteres."
      )
    return form

  def email_icon(self, obj):
    # return format_html('<i class="fa-solid fa-envelope email-icon"></i>')
    return format_html(' <p class=" email-icon" title="Correo Electronico">📧</p>')

  email_icon.short_description = 'Correo'

  def change_password_link(self, obj):
    if obj:
      return format_html('<a href="{}" class="button">Cambiar Contraseña</a>',
                         self.get_change_password_url(obj))
    return ""

  change_password_link.short_description = 'Acciones'

  def get_change_password_url(self, obj):
    return f"/admin/accounts/superuser/{obj.id}/password/"  # Asegúrate de que esta URL sea correcta

  # def get_fieldsets(self, request, obj=None):
  #   fieldsets = super().get_fieldsets(request, obj)
  #   if obj:  # Si estamos editando un superusuario existente
  #     # Mostrar permisos y grupos directamente
  #     fieldsets += (
  #       (_('Permisos'), {'fields': ('groups', 'user_permissions')}),
  #     )
  #   return fieldsets


# Configuración de User normal hacia Admin
class Usuario(BaseUserAdmin):
  # form = CustomUserChangeForm
  # add_form = CustomUserCreationForm
  # model = User

  list_display = ('email_icon', 'username', 'first_name', 'last_name', 'birth_day', 'is_active', 'change_password_link')
  list_filter = ('birth_day', 'is_active', 'is_staff')
  search_fields = ('email', 'username', 'first_name', 'last_name')
  ordering = ('email', 'username')
  ordering = ('email', 'username')
  readonly_fields = ('last_login', 'date_joined', 'password')

  # Formulario para actualizar un User
  fieldsets = (
    (_('Registro Usuario'), {'fields': ('email', 'username', 'password', 'is_active', 'is_staff')}),
    (_('Información Personal'), {'fields': ('first_name', 'last_name', 'birth_day')}),
    (_('Fechas Importantes'), {'fields': ('last_login', 'date_joined')}),
  )

  # Formulario para un nuevo User
  add_fieldsets = (
    (_('Registrando Nuevo Usuario'),
     {'classes': ('wide',), 'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff')}),
    (_('Información Personal'), {'fields': ('first_name', 'last_name', 'birth_day')}),
    (_('Fechas Importantes'), {'fields': ('last_login', 'date_joined')}),
  )

  class Media:
    css = {
      'all': ('css/adminDjango.css',)
    }

  def get_form(self, request, obj=None, **kwargs):
    """
          Agregacion de texto de ayuda, de acuerdo si se esta editando o creando un registro.
    """
    form = super(Usuario, self).get_form(request, obj, **kwargs)
    if obj:  # Si estamos editando un usuario existente
      form.base_fields['is_staff'].help_text = (
        "Actualmente tiene acceso, al panel de Administrador."
      )
    else:
      form.base_fields['is_staff'].help_text = (
        "Tendra acceso al panel de Administrador."
      )
    return form

  def email_icon(self, obj):
    # return format_html('<i class="fa-solid fa-envelope email-icon"></i>')
    return format_html(' <p class=" email-icon">📧</p>')

  email_icon.short_description = 'Correo'

  def change_password_link(self, obj):
    if obj:
      return format_html('<a href="{}" class="button">Cambiar Contraseña</a>', self.get_change_password_url(obj))
    return ""

  change_password_link.short_description = 'Acciones'

  def get_change_password_url(self, obj):
    return f"/admin/accounts/user/{obj.id}/password/"


# Configuración para administrar a User que pasaron a ser Admin
class AdminUserAdmin(admin.ModelAdmin):
  list_display = ('username', 'email', 'first_name', 'last_name', 'birth_day', 'list_roles')
  list_filter = ('roles',)
  search_fields = ('username', 'email', 'first_name', 'last_name')
  ordering = ('username', 'email')

  fieldsets = (
    (None, {'fields': ('username', 'email', 'password')}),
    (_('Información Personal'), {'fields': ('first_name', 'last_name', 'birth_day')}),
    (_('Roles'), {'fields': ('roles',)}),
  )

  filter_horizontal = ('roles',)

  def list_roles(self, obj):
    return ", ".join([role.name for role in obj.roles.all()])

  list_roles.short_description = "Roles"


# Registro de los modelos personalizados en el admin
admin.site.register(SuperUser, SuperUsuario)
admin.site.register(User, Usuario)
admin.site.register(UserAdmin, AdminUserAdmin)
