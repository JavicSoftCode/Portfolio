import datetime

from django.db import models


class Blog(models.Model):
  title = models.CharField(max_length=50)
  description = models.TextField()

  # para poder trabajar con imagenes se requiere instalar - pip install Pillow -
  image = models.ImageField(upload_to='app_my_blogs/images')
  date = models.DateField(default=datetime.date.today)

  def __str__(self) -> str:
    return self.title
