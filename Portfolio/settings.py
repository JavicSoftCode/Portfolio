import os
from pathlib import Path

# Para trabajar con variables de entorno se debe instalar
# pip install python-dotenv
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key')  # Usa un valor por defecto solo para desarrollo.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'  # Asegúrate de que sea 'False' en producción.

# Hosting permitidos
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# Application definition
INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',

  # My Apps
  'BackEnd.Apps.accounts.apps.AccountsConfig',
  'BackEnd.Apps.core.apps.CoreConfig',
  'BackEnd.Apps.My_Blogs.apps.MyBlogsConfig',
  'BackEnd.Apps.My_Portfolio_and_Projects.apps.MyPortfolioAndProjectsConfig',

]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  # My middleware
  # 'BackEnd.Apps.accounts.middleware.no_back_after_logout',  # VISTA BASADA EN FUNCIONES
  # 'BackEnd.Apps.accounts.middleware.NoBackAfterLogoutMiddleware',  # VISTA BASADA EN FUNCIONES
]

ROOT_URLCONF = 'Portfolio.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'FrontEnd/templates')],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',

      ],
    },
  },
]

WSGI_APPLICATION = 'Portfolio.wsgi.application'

# Configuracion de la Base de Datos
# pip install psycopg2-binary conector de la base de datos postgresql
DATABASES = {
  'default': {
    'ENGINE': os.getenv('DB_ENGINE', ''),
    'NAME': os.getenv('DB_NAME_DATABASE', ''),
    'USER': os.getenv('DB_USERNAME_DATABASE', ''),
    'PASSWORD': os.getenv('DB_PASSWORD_DATABASE', ''),
    'HOST': os.getenv('DB_HOST_DATABASE', ''),
    'PORT': os.getenv('DB_PORT_DATABASE', '5432'),
  }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {
      'min_length': 8,  # Asegúrate de que sea al menos 8 caracteres
    }
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-ec'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_TZ = True

# URL para acceder a los archivos estaticos ( CSS, JS )
STATIC_URL = '/static/'

# Ubicacion donde estara la carpeta de los archivos estaticos
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'FrontEnd/static')]

# URL para acceder y servir archivos
MEDIA_URL = '/public/'

# Ubicacion de la carpeta donde estaran los archivos subidos por el usuario
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Modelo de usuario personalizado
# AUTH_USER_MODEL = 'accounts.SuperUser'
AUTH_USER_MODEL = 'accounts.SuperUser'  # Asegúrate de que esta línea apunte a tu modelo de usuario

# Configuración de las URLs de inicio de sesión y cierre de sesión
LOGIN_URL = 'accounts:signin'  # Nombre de la URL para el inicio de sesión
LOGOUT_URL = 'accounts:signout'  # Nombre de la URL para el cierre de sesión
LOGIN_REDIRECT_URL = 'core:home'  # Cambia esto a la URL a la que deseas redirigir después del inicio de sesión
SIGNUP_REDIRECT_URL = 'accounts:signin'  # O la URL a la que quieras redirigir después del registro
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = False  # Redirigir a HTTPS
SESSION_COOKIE_SECURE = True  # Usar solo HTTPS para las cookies de sesión
CSRF_COOKIE_SECURE = True  # Usar solo HTTPS para la cookie CSRF
SECURE_HSTS_SECONDS = 3600  # O más, en segundos
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#
#
#
# AUTHENTICATION_BACKENDS = (
#     'accounts.backends.CustomUserBackend',  # Asegúrate de poner la ruta correcta
#     'django.contrib.auth.backends.ModelBackend',  # Para mantener el backend por defecto
# )

# from django.contrib.auth.backends import ModelBackend
# from .models import User, SuperUser
#
# class CustomUserBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             # Intenta autenticar un usuario normal
#             user = User.objects.get(email=username)
#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             pass
#
#         try:
#             # Intenta autenticar un superusuario
#             super_user = SuperUser.objects.get(email=username)
#             if super_user.check_password(password):
#                 return super_user
#         except SuperUser.DoesNotExist:
#             pass
#
#         return None
