from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .models import Blog


class BlogListView(LoginRequiredMixin, ListView):
  model = Blog
  template_name = 'appMy_Blogs/my_blogs.html'
  context_object_name = 'blogs'
  login_url = reverse_lazy('accounts:signin')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['total_blogs'] = self.get_queryset().count()
    context['title'] = 'My Blogs JSC'
    return context


class BlogsDetailView(LoginRequiredMixin, DetailView):
  model = Blog
  template_name = "appMy_Blogs/blog_details.html"
  context_object_name = "blog"
  login_url = reverse_lazy('accounts:signin')

  def get_object(self, **kwargs):
    blog_id = self.kwargs.get('blog_id')
    return get_object_or_404(Blog, pk=blog_id)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = self.object.title
    return context
