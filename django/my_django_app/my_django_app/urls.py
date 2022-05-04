"""my_django_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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


##### This is the project wide URLS.py which contains all urls #####
###### We also se subcategories of urls like tibiahelper/     ######
####### which includes one path to the tibiahelpers own urls #######
from django.contrib import admin
from django.urls import path, include

from website.views import welcome, date, about
from tibiahelper.views import get_creature_by_id, list_all_creatures

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name = "welcome"),
    path('date', date),
    path('about', about),
    path('tibiahelper/', include('tibiahelper.urls')) # Defines all the urls for tibiahelper pages
]
