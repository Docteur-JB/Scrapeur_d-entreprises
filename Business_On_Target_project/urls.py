"""
URL configuration for Business_On_Target_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path ,include
from auth_app import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
import os

def landing_page(request):
    """Servir la landing page statique"""
    landinng_path = os.path.join(settings.BASE_DIR, '..', 'bot-landing', 'index.html')
    with open(landinng_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content)

urlpatterns = [
    path('', landing_page, name='landing'),

    path('admin/', admin.site.urls),
    path('inscription/', views.inscription, name='inscription'),  # ← Plus de conflit
    path('business/', include('find_business.urls')),  # ← Préfixe dédié
    path('connexion/', views.connexion, name='connexion'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    path('home/', RedirectView.as_view(url='/', permanent=True))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)