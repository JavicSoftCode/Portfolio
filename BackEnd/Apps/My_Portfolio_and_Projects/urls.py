import hashlib

from django.urls import path, include

# @JavicSoftCode
from .views import PortfolioListView

app_name = 'My_Portfolio_and_Projects'


def generate_slug(text):
  return hashlib.md5(text.encode()).hexdigest()[:64]  # Un hash corto


urlpatterns = [
  path(f'p/{generate_slug("portfolio_and_projects")}/', PortfolioListView.as_view(), name='portfolio_and_projects'),
  path('accounts/', include('BackEnd.Apps.accounts.urls', namespace='accounts')),

]
