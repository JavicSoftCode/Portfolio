from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _


class Portfolio(models.Model):
  title = models.CharField(_('Título'), max_length=50)
  description = models.CharField(_('Descripción'), max_length=250)

  # para poder trabajar con imagenes se requiere instalar - pip install Pillow -
  image = models.ImageField(_('Subir IMG'), upload_to='app_my_portfolio_and_projects/images')
  url = models.URLField(_('Enlace -Link-'), blank=True)
  date = models.DateField(_('Fecha'), default=date.today)

  def __str__(self) -> str:
    return self.title

  class Meta:
    verbose_name = 'Proyecto'
    verbose_name_plural = 'Proyectos'


class Curso(models.Model):
  institution_of_the_course = models.CharField(_('Institución'), max_length=100)
  course_description = models.TextField(_('Descripción'))
  course_date = models.DateField(_('Fecha'))
  number_of_hours = models.PositiveIntegerField(_('Tiempo'))

  def __str__(self):
    return f'{self.institution_of_the_course}'

  class Meta:
    verbose_name = 'Curso'
    verbose_name_plural = 'Cursos'
