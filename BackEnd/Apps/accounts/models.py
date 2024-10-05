import random

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import ValidatorUser


# Manager personalizado para SuperUser
class CustomUserManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError('El campo de correo electrónico es obligatorio')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    if extra_fields.get('is_staff') is not True:
      raise ValueError('El superusuario debe tener is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('El superusuario debe tener is_superuser=True.')
    superuser = SuperUser(email=email, **extra_fields)
    superuser.set_password(password)
    superuser.save(using=self._db)
    return superuser

  def create_useradmin(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    if extra_fields.get('is_staff') is not True:
      raise ValueError('El usuario administrador debe tener is_staff=True.')
    return self.create_user(email, password, **extra_fields)


# Modelo de usuario personalizado
class CustomUser(AbstractUser):
  birth_day = models.DateField(_('Fecha Nacimiento'), validators=[ValidatorUser.validate_age])
  first_name = models.CharField(_('Nombre'), max_length=30, validators=[ValidatorUser.validate_full_name])
  last_name = models.CharField(_('Apellido'), max_length=30, validators=[ValidatorUser.validate_full_name])
  username = models.CharField(_('Usuario'), max_length=20, unique=True, validators=[ValidatorUser.validate_username])
  email = models.EmailField(_('Correo Electrónico'), unique=True, validators=[ValidatorUser.validate_email])
  is_staff = models.BooleanField(_('Admin'), default=False)
  is_active = models.BooleanField(_('Activo'), default=True)

  # Manager personalizado
  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['birth_day', 'first_name', 'last_name', 'username']

  class Meta:
    verbose_name = 'Usuario'
    verbose_name_plural = 'Usuarios'

  def email_user(self, subject, message, from_email=None, **kwargs):
    send_mail(subject, message, from_email, [self.email], **kwargs)

  @staticmethod
  def generate_random_code(length=8):
    """Genera un código aleatorio de 8 dígitos."""
    return ''.join(random.choices('0123456789', k=length))

  def __str__(self):
    return self.email or 'Usuario sin nombre'

  def assign_group(self, group):
    """Asigna un grupo al usuario."""
    self.groups.add(group)
    self.save()

  def remove_group(self, group):
    """Revoca un grupo del usuario."""
    self.groups.remove(group)
    self.save()

  def has_role(self, role):
    """Verifica si el usuario tiene un rol específico."""
    return self.groups.filter(name=role).exists()

  def assign_permission(self, permission):
    """Asigna un permiso al usuario."""
    self.user_permissions.add(permission)
    self.save()

  def remove_permission(self, permission):
    """Revoca un permiso del usuario."""
    self.user_permissions.remove(permission)
    self.save()

  @classmethod
  def get_custom_permissions(cls):
    return [
      ("can_view_users", "Puede ver usuarios"),
      ("can_edit_users", "Puede editar usuarios"),
      ("can_delete_users", "Puede eliminar usuarios"),
      ("can_promote_users", "Puede promover usuarios a administradores"),
    ]


class Role(models.Model):
  name = models.CharField(max_length=50, unique=True)

  def __str__(self):
    return self.name


class SuperUser(CustomUser):

  class Meta:
    verbose_name = 'Super Usuario'
    verbose_name_plural = 'Super Usuarios'


class User(CustomUser):
  class Meta:
    verbose_name = 'Usuario Normal'
    verbose_name_plural = 'Usuarios Normales'


class UserAdmin(CustomUser):
  roles = models.ManyToManyField(Role, blank=True)

  class Meta:
    verbose_name = 'Usuario Administrador'
    verbose_name_plural = 'Usuarios Administradores'
