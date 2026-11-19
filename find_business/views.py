from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
import subprocess
import sys

# views.py
from django.shortcuts import render
from .scrapeur import *  # tu importes ta fonction


@login_required(login_url='/connexion/')
def recherche_view(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword")
        try:
            # Appel de la fonction main avec le keyword
            results = main(keyword)  # ← keyword est passé ici

            return render(request, "info_business/index.html", {
                "entreprises": results,
                "keyword": keyword
            })

        except Exception as e:
            return render(request, "info_business/index.html", {
                "error": f"Erreur: {str(e)}",
                "keyword": keyword
            })

    return render(request, "info_business/index.html")