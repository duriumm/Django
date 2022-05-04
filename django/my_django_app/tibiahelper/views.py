from django.shortcuts import redirect, render, get_object_or_404
from django.forms import modelform_factory


from .models import Creature
from tibiahelper.webscraping.Creature_data import Webscraped_Creature
from tibiahelper.webscraping.Webscraper import get_creature_data, list_of_creatures_names



def get_creature_by_id(request, id):
  creature = get_object_or_404(Creature, pk = id)
  return render(request, "tibiahelper/get_creature_by_id.html", {"creature" : creature})

#def get_all_creatures(request):
 # all_creatures = Creature.objects.all(Creature, pk = id)
  #return render(request, "tibiahelper/get_creature_by_id.html", {"all_creatures" : all_creatures})

def list_all_creatures(request):
  return render(request, "tibiahelper/list_all_creatures.html", {
      "creatures" : Creature.objects.all()
      })


CreatureForm = modelform_factory(Creature, exclude = []) # A class 

## Webscrape + skapa objekt



def add_creatures_to_database():
  list_of_creatures = list_of_creatures_names()
  for creature in list_of_creatures:
    # if creature.startswith('E'):
    # if(creature == "Zushuka"):
    webscraped_creature = get_creature_data(creature)
    if(webscraped_creature is not None):
        print("--------------------In views processing creature: ", webscraped_creature.name)
        Creature.objects.create(
          name = webscraped_creature.name,
          health = webscraped_creature.health, 
          experience = webscraped_creature.experience, 
          speed = webscraped_creature.speed, 
          armor = webscraped_creature.armor, 
          maxdmg = webscraped_creature.maxdmg, 
          summon = webscraped_creature.summon, 
          convince = webscraped_creature.convince, 
          illusionable = webscraped_creature.illusionable, 
          pushable = webscraped_creature.pushable, 
          pushes = webscraped_creature.pushes, 
          killstounlock = webscraped_creature.killstounlock,
          senseinvis = webscraped_creature.senseinvis, 
          dmgfromphysical = webscraped_creature.dmgfromphysical, 
          dmgfromdeath = webscraped_creature.dmgfromdeath,
          dmgfromholy = webscraped_creature.dmgfromholy, 
          dmgfromice = webscraped_creature.dmgfromice, 
          dmgfromfire = webscraped_creature.dmgfromfire, 
          dmgfromenergy = webscraped_creature.dmgfromenergy, 
          dmgfromearth = webscraped_creature.dmgfromearth,
          listofloot = webscraped_creature.listofloot
        )
  #print("List of creature names: ", list_of_creatures)
  #webscraped_creature = get_creature_data("Amazon")




def new(request):
  add_creatures_to_database()
  # GET WEBSCRAPED CREATURE
  #webscraped_creature = get_creature_data("Amazon")
  #print("WEBSCRAPED CREATURE IS: ", webscraped_creature.name)
  #Creature.objects.create(name = "pellepong", health = 99, experience = 99, speed = 99, items = "Noneeee") # Creates new creature in DB
  if(request.method == "POST"):
    # form has been submitted, process data
    form = CreatureForm(request.POST)
    if(form.is_valid()):
      form.save()
      return redirect("welcome")
  else:
    form = CreatureForm()

  return render(request, "tibiahelper/new.html", { "form" : form })