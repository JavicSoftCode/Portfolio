import hashlib

from django.urls import path, include

# @JavicSoftCode
from .views import BlogListView, BlogsDetailView

app_name = 'My_Blogs'


def generate_slug(text):
  return hashlib.md5(text.encode()).hexdigest()[:64]  # Un hash corto


urlpatterns = [
  path(f'b/{generate_slug("blog_list")}/', BlogListView.as_view(), name='blog_list'),
  path(f'b/{generate_slug("blog_details")}/<int:blog_id>/', BlogsDetailView.as_view(), name='blog_details'),
  path('accounts/', include('BackEnd.Apps.accounts.urls', namespace='accounts')),

]
