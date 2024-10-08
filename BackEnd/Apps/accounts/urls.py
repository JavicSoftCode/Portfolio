from django.urls import path, include

from .views import SignInView, SignUpView, SignOutView

app_name = 'accounts'

urlpatterns = [
  path('', include('BackEnd.Apps.core.urls', namespace='core')),  # Core app URLs
  path('signup/', SignUpView.as_view(), name='signup'),  # Registro
  path('signin/', SignInView.as_view(), name='signin'),  # Inicio de sesión
  path('signout/', SignOutView.as_view(), name='signout'),  # Cierre de sesión
]
