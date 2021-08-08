"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.static import serve
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# Up two folders to serve "site" content
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.join(BASE_DIR, 'site')

urlpatterns = [
    path('', include('home.urls')),  # Change to ads.urls
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('hello',include('hello.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('autos/', include('autos.urls')),
    path('cats/', include('cats.urls')),
    path('myarts/', include('myarts.urls')),
    path('ads/', include('ads.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # Keep
    url(r'^site/(?P<path>.*)$', serve,
        {'document_root': SITE_ROOT, 'show_indexes': True},
        name='site_path'
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Serve the favicon - Keep for later
urlpatterns += [
    path('favicon.ico', serve, {
            'path': 'favicon.ico',
            'document_root': os.path.join(BASE_DIR, 'home/static'),
        }
    ),
]

# Switch to social login if it is configured - Keep for later
try:
    from .github_settings import *
    social_login = 'registration/login_social.html'
    urlpatterns.insert(0,
                       path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
                       )
    print('Using', social_login, 'as the login template')
except:
    print('Using registration/login.html as the login template')