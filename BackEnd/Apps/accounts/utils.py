from datetime import date
import re
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _


class ValidatorUser:

  @staticmethod
  def validate_age(birth_day):
    today = date.today()
    age = today.year - birth_day.year - ((today.month, today.day) < (birth_day.month, birth_day.day))
    if age < 18:  # o la edad mínima que desees
      raise ValidationError('El usuario debe ser mayor de 18 años.')

  @staticmethod
  def validate_full_name(value):
    MinLengthValidator(3, _("El nombre o apellido debe tener al menos 3 caracteres."))(value)

    words = value.split()
    if len(words) < 2 or any(len(word) < 2 for word in words):
      raise ValidationError(
        _("Debe ingresar al menos dos nombres o 2 apellidos, y cada uno debe tener al menos 2 caracteres."))

  @staticmethod
  def validate_username(username):
    """Valida el nombre de usuario."""
    MaxLengthValidator(20, _('Nombre de usuario maximo 10 caracteres'))
    if not re.match(r'^\w+$', username):
      raise ValidationError('El nombre de usuario solo puede contener letras, números y guiones bajos.')
    return username

  @staticmethod
  def validate_email(email):
    if "@" not in email:
      raise ValidationError(
        _('El correo electrónico debe contener un @.'),
        params={'email': email},
      )

  @staticmethod
  def validate_password(self, password):
    """Valida la contraseña."""
    if len(password) < 8:
      raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
    return password
