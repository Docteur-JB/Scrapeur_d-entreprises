from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import recherche_view

urlpatterns = [
    path('recherche/', login_required(recherche_view), name='recherche_view'), # ← le nom ici doit matcher
]