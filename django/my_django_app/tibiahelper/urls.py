from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>', views.get_creature_by_id, name = "get_creature_by_id"),
    path('list_all_creatures', views.list_all_creatures, name = "list_all_creatures"),
    path('new', views.new, name = "new"),

]