from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView

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


# Vista de inicio de sesión
class SignInView(LoginView):
  form_class = UserSignInForm
  template_name = 'appAccounts/signin.html'
  success_url = reverse_lazy('accounts:core:home')

  @method_decorator(never_cache)
  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect(self.success_url)
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    messages.success(self.request, '¡Has iniciado sesión exitosamente!')
    return super().form_valid(form)


# Vista de cierre de sesión
class SignOutView(LoginRequiredMixin, LogoutView):
  next_page = reverse_lazy('accounts:core:home')

  @method_decorator(never_cache)
  def dispatch(self, request, *args, **kwargs):
    messages.success(request, '¡Has cerrado sesión exitosamente!')
    response = super().dispatch(request, *args, **kwargs)
    logout(request)
    return response


# Vista para cambiar la contraseña
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
  form_class = UserSignUpForm
  template_name = 'appAccounts/resetPassword.html'
  success_url = reverse_lazy('accounts:core:home')

  @method_decorator(never_cache)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    messages.success(self.request, '¡Tu contraseña ha sido actualizada exitosamente!')
    return super().form_valid(form)
