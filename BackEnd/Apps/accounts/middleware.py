from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.deprecation import MiddlewareMixin


class NoBackAfterLogoutMiddleware(MiddlewareMixin):
  def process_request(self, request):
    return None if request.user.is_authenticated else HttpResponseRedirect(reverse_lazy('accounts:signin'))

#
# from django.http import HttpResponseRedirect
# from django.urls import reverse_lazy


# def no_back_after_logout(get_response):
#   def middleware(request):
#     # Verifica si el usuario no está autenticado
#     if not request.user.is_authenticated:
#       # Redirige a la página de inicio de sesión
#       return HttpResponseRedirect(reverse_lazy('accounts:signin'))
#
#     # Redirige según el rol del usuario
#     if request.user.is_superuser:
#       return HttpResponseRedirect(reverse_lazy('admin:panel'))  # URL del panel de superusuario
#     elif request.user.is_staff:
#       return HttpResponseRedirect(reverse_lazy('admin:roles'))  # URL para administradores
#     else:
#       return HttpResponseRedirect(reverse_lazy('core:home'))  # URL para usuarios normales
#
#     # return get_response(request)  # Continúa con la solicitud si el usuario está autenticado
#
#   return middleware
