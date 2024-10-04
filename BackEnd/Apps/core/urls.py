# from django.urls import path
# from .views import HomeTemplateView
#
# app_name = 'core'
#
# urlpatterns = [
#   path('', HomeTemplateView.as_view(), name='home'),
# ]
import hashlib
from django.urls import path

from .views import HomeTemplateView

app_name = 'core'


def generate_slug(text):
  return hashlib.md5(text.encode()).hexdigest()[:64]  # Un hash corto


urlpatterns = [
  path('', HomeTemplateView.as_view(), name='home'),
]
