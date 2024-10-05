import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


class Blog(models.Model):
  title = models.CharField(_('Título'), max_length=50)
  description = models.TextField(_('Descripción'))

  # para poder trabajar con imagenes se requiere instalar - pip install Pillow -
  image = models.ImageField(_('Subir IMG'), upload_to='app_my_blogs/images')
  date = models.DateField(_('Fecha'), default=datetime.date.today)

  def __str__(self) -> str:
    return self.title

  class Meta:
    verbose_name = 'Blog'
    verbose_name_plural = 'Blogs'
