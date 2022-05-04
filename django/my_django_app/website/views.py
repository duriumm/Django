from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

from tibiahelper.models import Creature

def welcome(request):
    return render(request, "website/welcome.html", {
        "message" : "This data was sent from the view to the template",
        "creatures" : Creature.objects.all()
        })

def date(request):
    return HttpResponse(f"This page was served at {str(datetime.now())}")

def about(request):
    return HttpResponse(f"I am 29 years old and my name is Lasse")


