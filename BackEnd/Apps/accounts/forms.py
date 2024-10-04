from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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
  username = forms.EmailField(label="Correo Electrónico")

  class Meta:
    model = User
    fields = ('username', 'password')

  def clean(self):
    cleaned_data = super().clean()
    username = cleaned_data.get('username')
    password = cleaned_data.get('password')

    if username and password:
      user = authenticate(username=username, password=password)
      if user is None:
        raise forms.ValidationError(_('Las credenciales son incorrectas.'))

    return cleaned_data

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field_name, field in self.fields.items():
      field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})
      field.widget.attrs.update({'style': 'border-radius: 0.25rem; padding: 0.5rem;'})
