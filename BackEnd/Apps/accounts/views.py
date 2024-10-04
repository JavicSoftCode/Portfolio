from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
# from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import render


# from .forms import UserSignInForm
from .forms import UserSignUpForm, UserSignInForm
from .models import User


# Vista de registro
class SignUpView(CreateView):
  model = User
  form_class = UserSignUpForm
  template_name = 'appAccounts/signup.html'
  success_url = reverse_lazy('accounts:signin')

  def form_valid(self, form):
    user = form.save()
    login(self.request, user)  # Inicia sesión automáticamente al registrarse
    messages.success(self.request, '¡Te has registrado exitosamente!')
    return redirect(self.success_url)

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class SignInView(LoginView):
  form_class = UserSignInForm
  template_name = 'appAccounts/signin.html'
  success_url = reverse_lazy('accounts:core:home')  # Verifica que la URL sea correcta

  def dispatch(self, request, *args, **kwargs):
    # Si el usuario ya está autenticado, redirige a la página de inicio
    if request.user.is_authenticated:
      return redirect(self.success_url)  # Usa success_url aquí

    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    # Autenticar al usuario y guardar la sesión
    email = form.cleaned_data.get('email')
    password = form.cleaned_data.get('password')
    user = authenticate(request=self.request, username=email, password=password)

    if user is not None:
      login(self.request, user)
      messages.success(self.request, '¡Has iniciado sesión exitosamente!')
      return redirect(self.success_url)  # Redirige a la página de inicio
    else:
      messages.error(self.request, 'Las credenciales son incorrectas.')
      return self.form_invalid(form)


# Vista de cierre de sesión
class SignOutView(LoginRequiredMixin, LogoutView):
  next_page = reverse_lazy('accounts:core:home')

  @method_decorator(never_cache)
  def dispatch(self, request, *args, **kwargs):
    messages.success(request, '¡Has cerrado sesión exitosamente!')
    response = super().dispatch(request, *args, **kwargs)
    logout(request)  # Cerrar sesión para eliminar cookies
    return response


# Vista para cambiar la contraseña
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
  form_class = UserSignUpForm  # Cambia esto a tu formulario de cambio de contraseña
  template_name = 'appAccounts/resetPassword.html'
  success_url = reverse_lazy('accounts:core:home')

  def form_valid(self, form):
    messages.success(self.request, '¡Tu contraseña ha sido actualizada exitosamente!')
    return super().form_valid(form)
