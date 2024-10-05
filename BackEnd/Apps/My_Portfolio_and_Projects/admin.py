from django.contrib import admin
from django.utils.html import format_html

from .models import Portfolio, Curso


class PortfolioAdmin(admin.ModelAdmin):
  list_display = (
    'visualize_icon', 'thumbnail_image', 'title', 'short_description', 'url_icon', 'date', 'action_buttons')
  list_display_links = None
  search_fields = ('title',)
  list_filter = ()

  class Media:
    css = {
      'all': ('css/adminDjango.css',)
    }

  def __init__(self, model, admin_site):
    super().__init__(model, admin_site)
    self.request = None

  def url_icon(self, obj):
    """Añade un icono que, al hacer clic, abre el enlace del proyecto en una nueva pestaña"""
    return format_html(
      '<a href="{}" target="_blank" class="button"><i class="fa-solid fa-arrow-up-right-from-square"></i></a>',
      obj.url
    )

  url_icon.short_description = 'Enlace'

  def visualize_icon(self, obj):
    """Añade un icono de ojo que llevará a la página de detalles del proyecto"""
    return format_html(
      '<a href="{}" title="Visualizar" class="button"><i class="fa-solid fa-eye"></i></a>',
      self.get_detail_url(obj)
    )

  visualize_icon.short_description = 'Visualizar'

  def thumbnail_image(self, obj):
    """Muestra la imagen del proyecto redimensionada a 50px x 50px"""
    return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)

  thumbnail_image.short_description = 'Imagen'

  def short_description(self, obj):
    """Muestra los primeros 50 caracteres de la descripción"""
    return format_html('{}...', obj.description[:50])

  short_description.short_description = 'Descripción'

  def action_buttons(self, obj):
    """Crea botones de acción para editar y eliminar el proyecto"""
    return format_html(
      '<a href="{}" class="button" title="Editar">'
      '<i class="fa-solid fa-pencil-alt"></i></a>'
      '&nbsp;<a href="{}" class="button" title="Eliminar" onclick="return confirm(\'¿Está seguro de eliminar este Proyecto?\')">'
      '<i class="fa-solid fa-trash"></i></a>',
      self.get_edit_url(obj),
      self.get_delete_url(obj)
    )

  action_buttons.short_description = 'Acciones'

  def get_detail_url(self, obj):
    """Devuelve la URL de detalle del proyecto"""
    return f"/admin/My_Portfolio_and_Projects/portfolio/{obj.id}/change/?readonly=true"

  def get_edit_url(self, obj):
    """Devuelve la URL para editar el proyecto"""
    return f"/admin/My_Portfolio_and_Projects/portfolio/{obj.id}/change/"

  def get_delete_url(self, obj):
    """Devuelve la URL para eliminar el proyecto"""
    return f"/admin/My_Portfolio_and_Projects/portfolio/{obj.id}/delete/"

  def get_queryset(self, request):
    """Asegura que request esté disponible en otros métodos"""
    self.request = request
    return super().get_queryset(request)

  def get_readonly_fields(self, request, obj=None):
    if 'readonly' in request.GET:
      return [f.name for f in self.model._meta.fields]
    return super().get_readonly_fields(request, obj)


class CursoAdmin(admin.ModelAdmin):
  list_display = ('visualize_icon', 'institution_of_the_course', 'short_description', 'course_date', 'number_of_hours',
                  'action_buttons')
  list_display_links = None
  search_fields = ('institution_of_the_course',)
  list_filter = ()

  class Media:
    css = {
      'all': ('css/adminDjango.css',)
    }

  def __init__(self, model, admin_site):
    super().__init__(model, admin_site)
    self.request = None

  def visualize_icon(self, obj):
    """Añade un icono de ojo que llevará a la página de detalles del curso en modo readonly"""
    return format_html(
      '<a href="{}" title="Visualizar" class="button"><i class="fa-solid fa-eye"></i></a>',
      self.get_detail_url(obj)
    )

  visualize_icon.short_description = 'Visualizar'

  def short_description(self, obj):
    """Muestra los primeros 50 caracteres de la descripción del curso"""
    return format_html('{}...', obj.course_description[:50])

  short_description.short_description = 'Descripción'

  def action_buttons(self, obj):
    """Crea botones de acción para editar y eliminar el curso"""
    return format_html(
      '<a href="{}" class="button" title="Editar">'
      '<i class="fa-solid fa-pencil-alt"></i></a>'
      '&nbsp;<a href="{}" class="button" title="Eliminar" onclick="return confirm(\'¿Está seguro de eliminar este curso?\')">'
      '<i class="fa-solid fa-trash"></i></a>',
      self.get_edit_url(obj),
      self.get_delete_url(obj)
    )

  action_buttons.short_description = 'Acciones'

  def get_detail_url(self, obj):
    """Devuelve la URL de detalle del curso"""
    return f"/admin/My_Portfolio_and_Projects/curso/{obj.id}/change/?readonly=true"

  def get_edit_url(self, obj):
    """Devuelve la URL para editar el curso"""
    return f"/admin/My_Portfolio_and_Projects/curso/{obj.id}/change/"

  def get_delete_url(self, obj):
    """Devuelve la URL para eliminar el curso"""
    return f"/admin/My_Portfolio_and_Projects/curso/{obj.id}/delete/"

  def get_queryset(self, request):
    """Asegura que request esté disponible en otros métodos"""
    self.request = request
    return super().get_queryset(request)

  def get_readonly_fields(self, request, obj=None):
    """Establece los campos como readonly cuando está en modo visualización"""
    if 'readonly' in request.GET:
      return [f.name for f in self.model._meta.fields]
    return super().get_readonly_fields(request, obj)


# Registramos el modelo Portafolio y Curso con la configuración personalizada
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Curso, CursoAdmin)
