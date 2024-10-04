from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from .models import User


class UserSignUpForm(UserCreationForm):
  email = forms.EmailField(required=True, label='Correo Electrónico')

  class Meta:
    model = User
    fields = ('email', 'first_name', 'last_name', 'username', 'birth_day', 'password1', 'password2')

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError('Ya existe un usuario con este correo electrónico.')
    return email

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Agrega la clase de Bootstrap a las etiquetas y a los campos
    for field_name, field in self.fields.items():
      field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})  # Clase para Bootstrap
      # Adicionalmente, puedes personalizar el tamaño y el borde de los inputs
      field.widget.attrs.update({'style': 'border-radius: 0.25rem; padding: 0.5rem; color:black;'})


class UserSignInForm(AuthenticationForm):
  email = forms.EmailField(label="Correo Electrónico")

  class Meta:
    model = User
    fields = ('email', 'password')

  def clean(self):
    cleaned_data = super().clean()
    email = cleaned_data.get('email')
    password = cleaned_data.get('password')

    if email and password:
      # Cambia el username por el email
      user = authenticate(request=self.request, username=email, password=password)  # Asegúrate de pasar el request aquí
      if user is None:
        raise forms.ValidationError(_('Las credenciales son incorrectas.'))

    return cleaned_data


class CustomPasswordChangeForm(PasswordChangeForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
    self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
    self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
