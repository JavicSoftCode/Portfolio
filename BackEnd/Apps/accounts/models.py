from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import ValidatorUser


# Manager personalizado para SuperUser
class SuperUserManager(BaseUserManager):
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

    return self.create_user(email, password, **extra_fields)


# Modelo para SuperUser campos propios del SuperUser Modificados y campos extras agregados
class SuperUser(AbstractUser):
  birth_day = models.DateField(_('Fecha Nacimiento'), validators=[ValidatorUser.validate_age])
  first_name = models.CharField(_('Nombre'), max_length=30, validators=[ValidatorUser.validate_full_name])
  last_name = models.CharField(_('Apellido'), max_length=30, validators=[ValidatorUser.validate_full_name])
  username = models.CharField(_('Usuario'), max_length=20, unique=True, validators=[ValidatorUser.validate_username])
  email = models.EmailField(_('Correo Electrónico'), unique=True, validators=[ValidatorUser.validate_email])
  is_staff = models.BooleanField(_('Admin'), default=True)
  is_superuser = models.BooleanField(_('Super User'), default=True)

  # Asignar el manager personalizado
  objects = SuperUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['birth_day', 'first_name', 'last_name', 'username']

  class Meta:
    verbose_name = 'Super Usuario'
    verbose_name_plural = 'Super Usuarios'

  def email_user(self, subject, message, from_email=None, **kwargs):
    send_mail(subject, message, from_email, [self.email], **kwargs)

  @staticmethod
  def generate_random_code(length=8):
    """Genera un código aleatorio de 8 dígitos."""
    return ''.join(random.choices('0123456789', k=length))

  def promote_user_to_admin(self, user):
    """
    Promueve un usuario normal a UserAdmin.
    """
    user_admin = UserAdmin.objects.create(
      username=user.username,
      email=user.email,
      birth_day=user.birth_day,
      first_name=user.first_name,
      last_name=user.last_name,
      is_superuser=user.is_superuser,
      is_staff=user.is_staff
    )
    user_admin.is_staff = True
    user_admin.save()
    user.delete()  # Elimina el usuario original


# Modelo para usuarios normales (User)
class User(AbstractUser):
  birth_day = models.DateField(_('Fecha Nacimiento'), validators=[ValidatorUser.validate_age])
  first_name = models.CharField(_('Nombre'), max_length=30, validators=[ValidatorUser.validate_full_name])
  last_name = models.CharField(_('Apellido'), max_length=30, validators=[ValidatorUser.validate_full_name])
  username = models.CharField(_('Usuario'), max_length=20, unique=True, validators=[ValidatorUser.validate_username])
  email = models.EmailField(_('Correo Electrónico'), unique=True, validators=[ValidatorUser.validate_email])
  is_staff = models.BooleanField(_('Admin'), default=False)
  is_active = models.BooleanField(_('Activo'), default=True)
  groups = models.ManyToManyField(
    Group,
    related_name='user_set_custom',  # Cambia el nombre aquí
    blank=True,
    help_text=_('Grupos a los que este usuario pertenece.'),
    verbose_name=_('Grupos'),
  )

  user_permissions = models.ManyToManyField(
    Permission,
    related_name='user_set_custom',  # Cambia el nombre aquí
    blank=True,
    help_text=_('Permisos específicos de este usuario.'),
    verbose_name=_('Permisos'),
  )

  USERNAME_FIELD = 'email'

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
    return self.username

  def save(self, *args, **kwargs):
    # Encriptar la contraseña si es nueva o ha sido modificada
    if not self.pk or not User.objects.filter(pk=self.pk, password=self.password).exists():
      self.password = make_password(self.password)
    super(User, self).save(*args, **kwargs)

  def __str__(self):
    # Asegúrate de que el nombre o el correo no sean None
    return self.email or 'Usuario sin nombre'


# Modelo para UserAdmin, activado cuando un SuperUser promueve a un User
class UserAdmin(User):
  roles = models.ManyToManyField(Group, related_name='user_admin_roles', blank=True)

  class Meta:
    verbose_name = 'Administrador de Usuario'
    verbose_name_plural = 'Administradores de Usuario'

  def email_user(self, subject, message, from_email=None, **kwargs):
    send_mail(subject, message, from_email, [self.email], **kwargs)

  @staticmethod
  def generate_random_code(length=8):
    """Genera un código aleatorio de 8 dígitos."""
    return ''.join(random.choices('0123456789', k=length))

  def assign_role(self, role):
    """
    Asigna un rol a este UserAdmin.
    """
    self.roles.add(role)
    self.save()

  def revoke_role(self, role):
    """
    Revoca un rol de este UserAdmin.
    """
    self.roles.remove(role)
    self.save()

  def __str__(self):
    # Asegúrate de que el nombre o el correo no sean None
    return self.email or 'Usuario sin nombre'
