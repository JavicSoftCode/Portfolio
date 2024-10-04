from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                path('admin/', admin.site.urls),
                path('', include('BackEnd.Apps.core.urls', namespace='core')),
                path('blogs/', include('BackEnd.Apps.My_Blogs.urls', namespace='My_Blogs')),
                path('portfolio_and_projects/',
                     include('BackEnd.Apps.My_Portfolio_and_Projects.urls', namespace='My_Portfolio_and_Projects')),
                path('accounts/', include('BackEnd.Apps.accounts.urls', namespace='accounts')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
