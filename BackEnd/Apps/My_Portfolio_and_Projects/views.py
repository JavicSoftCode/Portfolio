from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .models import Portfolio, Curso


class PortfolioAndCursoTemplateView(LoginRequiredMixin, TemplateView):
  template_name = 'appMy_Portfolio_and_Projects/my_portfolio_and_projects.html'
  login_url = reverse_lazy('accounts:signin')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Portfolio and Projects and Courses'
    context['projects'] = Portfolio.objects.all()
    context['cursos'] = Curso.objects.all()
    return context
