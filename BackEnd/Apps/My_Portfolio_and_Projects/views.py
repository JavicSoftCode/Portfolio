# from django.views.generic import ListView
#
# # @JavicSoftCode
# from .models import Portfolio
#
#
# class PortfolioListView(ListView):
#   model = Portfolio
#   template_name = 'appMy_Portfolio_and_Projects/my_portfolio_and_projects.html'
#   context_object_name = 'projects'
#
#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['title'] = 'My Portfolio JSC'
#     return context


from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView

from .models import Portfolio


class PortfolioListView(LoginRequiredMixin, ListView):
  model = Portfolio
  template_name = 'appMy_Portfolio_and_Projects/my_portfolio_and_projects.html'
  context_object_name = 'projects'
  login_url = reverse_lazy('accounts:signin')  # Redirige a la página de inicio de sesión

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'My Portfolio JSC'
    return context
