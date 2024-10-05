from django.contrib import admin
from django.utils.html import format_html

from .models import Blog


class BlogAdmin(admin.ModelAdmin):
  list_display = ('visualize_icon', 'thumbnail_image', 'title', 'short_description', 'date', 'action_buttons')
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

  def visualize_icon(self, obj):
    """Añade un icono de ojo que llevará a la página de detalles del blog"""
    return format_html(
      '<a href="{}" title="Visualizar" class="button"><i class="fa-solid fa-eye"></i></a>',
      self.get_detail_url(obj)
    )

  visualize_icon.short_description = 'Visualizar'

  def thumbnail_image(self, obj):
    """Muestra la imagen del blog redimensionada a 50px x 50px"""
    return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)

  thumbnail_image.short_description = 'Imagen'

  def short_description(self, obj):
    """Muestra los primeros 10 caracteres de la descripción"""
    return format_html('{}...', obj.description[:50])

  short_description.short_description = 'Descripción'

  def action_buttons(self, obj):
    """Crea botones de acción para editar y eliminar el blog"""
    return format_html(
      '<a href="{}" class="button" title="Editar">'
      '<i class="fa-solid fa-pencil-alt"></i></a>'
      '&nbsp;<a href="{}" class="button" title="Eliminar" onclick="return confirm(\'¿Está seguro de eliminar este Blog?\')">'
      '<i class="fa-solid fa-trash"></i></a>',
      self.get_edit_url(obj),
      self.get_delete_url(obj)
    )

  action_buttons.short_description = 'Acciones'

  def get_detail_url(self, obj):
    """Devuelve la URL de detalle del blog"""
    return f"/admin/My_Blogs/blog/{obj.id}/change/?readonly=true"

  def get_edit_url(self, obj):
    """Devuelve la URL para editar el blog"""
    return f"/admin/My_Blogs/blog/{obj.id}/change/"

  def get_delete_url(self, obj):
    """Devuelve la URL para eliminar el blog"""
    return f"/admin/My_Blogs/blog/{obj.id}/delete/"

  def get_queryset(self, request):
    """Asegura que request esté disponible en otros métodos"""
    self.request = request
    return super().get_queryset(request)

  def get_readonly_fields(self, request, obj=None):
    if 'readonly' in request.GET:
      return [f.name for f in self.model._meta.fields]
    return super().get_readonly_fields(request, obj)


# Registramos el modelo Blog con la configuración personalizada
admin.site.register(Blog, BlogAdmin)
