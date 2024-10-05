from django.contrib import admin
from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
  class Media:
    css = {
      'all': ('css/adminDjango.css',)
    }


# Desregistramos el admin original de User y lo volvemos a registrar con nuestra configuración
admin.site.unregister(User)
