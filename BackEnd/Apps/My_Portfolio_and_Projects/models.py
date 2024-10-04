from datetime import date

from django.db import models


class Portfolio(models.Model):
  title = models.CharField(max_length=50)
  description = models.CharField(max_length=250)

  # para poder trabajar con imagenes se requiere instalar - pip install Pillow -
  image = models.ImageField(upload_to='app_my_portfolio_and_projects/images')
  url = models.URLField(blank=True)
  date = models.DateField(default=date.today)

  def __str__(self) -> str:
    return self.title
