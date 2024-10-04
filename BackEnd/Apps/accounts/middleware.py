from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.deprecation import MiddlewareMixin


class NoBackAfterLogoutMiddleware(MiddlewareMixin):
  def process_request(self, request):
    return None if request.user.is_authenticated else HttpResponseRedirect(reverse_lazy('accounts:signin'))
