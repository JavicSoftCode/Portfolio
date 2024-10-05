from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import SuperUser, User, UserAdmin


# Configuración del admin para SuperUser
class SuperUsuario(BaseUserAdmin):
  list_display = ('email_icon', 'username', 'first_name', 'last_name', 'birth_day', 'is_active', 'action_buttons')
  list_display_links = None
  search_fields = ('email', 'username', 'first_name', 'last_name')
  ordering = ('email', 'username')
  readonly_fields = ('last_login', 'date_joined', 'password')

  list_filter = ()

  fieldsets = (
    (_('Registro Super Usuario'),
     {'fields': ('email', 'username', 'password', 'is_active', 'is_staff', 'is_superuser')}),
    (_('Información Personal'), {'fields': ('first_name', 'last_name', 'birth_day')}),
    (_('Fechas Importantes'), {'fields': ('last_login', 'date_joined')}),
    (_('Permisos'), {'fields': ('groups', 'user_permissions')}),
  )

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

  def __init__(self, model, admin_site):
    super().__init__(model, admin_site)
    self.request = None

  def email_icon(self, obj):
    current_user = self.request.user

    email = obj.email
    subject = "Administrador de Django"
    body = f"Buen Día, le saluda {current_user.first_name} {current_user.last_name}"

    gmail_url = (
      f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={subject}&body={body}&tf=1"
    )

    return format_html('<a href="{}" target="_blank"><i class="fa-solid fa-envelope email-icon"></i></a>', gmail_url)

  email_icon.short_description = 'Correo'

  def action_buttons(self, obj):
    return format_html(
      '<a href="{}" class="button" title="Actualizar contraseña">'
      '<i class="fa-solid fa-key"></i></a>'
      '&nbsp;<a href="{}" class="button" title="Editar">'
      '<i class="fa-solid fa-pencil-alt"></i></a>'
      '&nbsp;<a href="{}" class="button" title="Eliminar" onclick="return confirm(\'¿Está seguro de eliminar este Super Usuario?\')">'
      '<i class="fa-solid fa-trash"></i></a>',
      self.get_change_password_url(obj),
      self.get_edit_url(obj),
      self.get_delete_url(obj)
    )

  action_buttons.short_description = 'Acciones'

  def get_change_password_url(self, obj):
    return f"/admin/accounts/superuser/{obj.id}/password/"

  def get_edit_url(self, obj):
    return f"/admin/accounts/superuser/{obj.id}/change/"

  def get_delete_url(self, obj):
    return f"/admin/accounts/superuser/{obj.id}/delete/"

  def response_add(self, request, obj, post_url_continue=None):
    if "_addanother" in request.POST:
      return super().response_add(request, obj, post_url_continue)
    else:
      return self.response_post_save_change(request, obj)

  def get_queryset(self, request):
    self.request = request
    return super().get_queryset(request)


# Configuración para User normal hacia Admin
class Usuario(BaseUserAdmin):
  list_display = ('email_icon', 'username', 'first_name', 'last_name', 'birth_day', 'is_active', 'action_buttons')
  list_display_links = None
  search_fields = ('email', 'username', 'first_name', 'last_name')
  ordering = ('email', 'username')
  readonly_fields = ('last_login', 'date_joined', 'password')

  list_filter = ()

  fieldsets = (
    (_('Registro Usuario'), {'fields': ('email', 'username', 'password', 'is_active', 'is_staff')}),
    (_('Información Personal'), {'fields': ('first_name', 'last_name', 'birth_day')}),
    (_('Fechas Importantes'), {'fields': ('last_login', 'date_joined')}),
  )

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

  def __init__(self, model, admin_site):
    super().__init__(model, admin_site)
    self.request = None

  def email_icon(self, obj):
    current_user = self.request.user

    email = obj.email
    subject = "Administrador de Django"
    body = f"Buen Día, le saluda {current_user.first_name} {current_user.last_name}"

    gmail_url = (
      f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={subject}&body={body}&tf=1"
    )

    return format_html('<a href="{}" target="_blank" class="button"><i class="fa-solid fa-envelope email-icon"></i></a>', gmail_url)

  email_icon.short_description = 'Correo'

  def action_buttons(self, obj):
    return format_html(
      '<a href="{}" class="button" title="Actualizar contraseña">'
      '<i class="fa-solid fa-key"></i></a>'
      '&nbsp;<a href="{}" class="button" title="Editar">'
      '<i class="fa-solid fa-pencil-alt"></i></a>'
      '&nbsp;<a href="{}" class="button" title="Eliminar" onclick="return confirm(\'¿Está seguro de eliminar este Usuario?\')">'
      '<i class="fa-solid fa-trash"></i></a>',
      self.get_change_password_url(obj),
      self.get_edit_url(obj),
      self.get_delete_url(obj)
    )

  action_buttons.short_description = 'Acciones'

  def get_change_password_url(self, obj):
    return f"/admin/accounts/user/{obj.id}/password/"

  def get_edit_url(self, obj):
    return f"/admin/accounts/user/{obj.id}/change/"

  def get_delete_url(self, obj):
    return f"/admin/accounts/user/{obj.id}/delete/"

  def response_add(self, request, obj, post_url_continue=None):
    if "_addanother" in request.POST:
      return super().response_add(request, obj, post_url_continue)
    else:
      return self.response_post_save_change(request, obj)

  def get_queryset(self, request):
    self.request = request
    return super().get_queryset(request)


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

  class Media:
    css = {
      'all': ('css/adminDjango.css',)
    }

  def list_roles(self, obj):
    return ", ".join([role.name for role in obj.roles.all()])

  list_roles.short_description = "Roles"


# Registro de los modelos personalizados en el admin
admin.site.register(SuperUser, SuperUsuario)
admin.site.register(User, Usuario)
admin.site.register(UserAdmin, AdminUserAdmin)
