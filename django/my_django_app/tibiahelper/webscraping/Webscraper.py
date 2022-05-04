# Webscraper to get the list of enemy names on tibia.fandom.com
import requests
from bs4 import BeautifulSoup
import time
from tibiahelper.webscraping.Creature_data import Webscraped_Creature
import re

# TODO: Make this function return the list of creature names
def list_of_creatures_names():
  tick = time.perf_counter()

  URL = "https://tibia.fandom.com/wiki/List_of_Creatures"

  page = requests.get(URL)

  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find(id="mw-content-text")

  html_enemy_names = results.find_all("tr")

  enemy_names_list = []

  for html_enemy in html_enemy_names:
    for td in html_enemy.find_all('td'):
      actual_enemy_name = td.get_text()
      actual_enemy_name.strip()
      enemy_names_list.append(actual_enemy_name)
      break # Break since we are taking first object only (Name) and then returning

  #print(len(enemy_names_list))

  tock = time.perf_counter()

  elapsed_time = tock - tick
  #print(elapsed_time)
  return enemy_names_list


def get_creature_data(creature_name):

  ignore_list = ["Food Wagon", "Lost Ghost of a Planegazer", "Pig (Nostalgia)", "Time Travelling Tourist", "Used Food Wagon"]
  if(creature_name in ignore_list):
    print(f"Ignored {creature_name} since its attributes are broken")
    return None

  URL = f"https://tibia.fandom.com/wiki/{creature_name}"
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find(class_="portable-infobox")
  enemy_attributes = results.findAll("div", "pi-item")

  creature_attributes_list = []

  #print("We are processing creature: ", creature_name)
  
  ################ GET ALL DATA EXCEPT RESISTANCE & LOOT FOR CREATURE ################
  for attribute in enemy_attributes:
    try:
      creature_attribute = attribute.get_text()
      creature_attribute = creature_attribute.strip()
      creature_attributes_list.append(creature_attribute)
    except:
        return None
    

  not_needed_attributes = ["Classification", "Spawn Type", "Class", "Walks Around", "Version", "Status", "Charm Points"]
  final_creature_dict = {}

  for x in creature_attributes_list:
    if("\n" in x):
      data = x.split("\n")
      if(data[1] == '✓'):
        data[1] = "Yes"
      elif(data[1] == '✗'):
        data[1] = "No"
      elif(data[0] in not_needed_attributes):
        creature_attributes_list.remove(x)
        continue
      final_creature_dict[data[0]] = data[1] # Adding new {key : value} pair to dict 
      #print(f"Creature data:  {data[0]} - {data[1]}")
    else:
      #print(f"removing {x} since it didnt have backslash n")
      creature_attributes_list.remove(x)

  ################ CLEAN EXPERIENCE NUMBERS ################ 
  if(final_creature_dict.get("Experience") == "Unknown." or final_creature_dict.get("Experience") == "Unknown"):
    final_creature_dict["Experience"] = None

  clean_experience_str = ''
  if(final_creature_dict.get("Experience") is not None):
    for char in final_creature_dict.get("Experience"):
      if char.isdigit():
        clean_experience_str += char
    final_creature_dict["Experience"] = clean_experience_str

  if(final_creature_dict.get("Experience") == '?' or
  final_creature_dict.get("Experience") == '' or
  final_creature_dict.get("Experience") == 'Unknown' or
  final_creature_dict.get("Experience") == 'Unknown.'):
    final_creature_dict["Experience"] = None
  ################ CLEAN EXPERIENCE NUMBERS ################ 

  ################ CLEAN MAX DMG NUMBERS ################ 
  #print(f"MAXDMG burster before cleaning is: {final_creature_dict.get('Est. Max Dmg')}")

  if('?' in final_creature_dict.get("Est. Max Dmg")):
    max_dmg = final_creature_dict.get("Est. Max Dmg").split('?')
    final_creature_dict["Est. Max Dmg"] = max_dmg[0]
  elif(len(final_creature_dict.get("Est. Max Dmg")) > 6):
    final_creature_dict["Est. Max Dmg"] = final_creature_dict.get("Est. Max Dmg").split(" ")[0]
  
  #print(f"MAXDMG burster 1 cleaning is: {final_creature_dict.get('Est. Max Dmg')}")

  ## Get the number from a string like this: "5000+ (2000+\xa0, 3000+\xa0)". We want 5000 only here
  if (len(final_creature_dict.get("Est. Max Dmg")) > 6):
    split_maxdmg = final_creature_dict["Est. Max Dmg"].split(" ")[0].replace('+', '')
    final_creature_dict["Est. Max Dmg"] = split_maxdmg

  #print(f"MAXDMG burster 2 cleaning is: {final_creature_dict.get('Est. Max Dmg')}")

  if(final_creature_dict.get("Est. Max Dmg") == '?' or
    final_creature_dict.get("Est. Max Dmg") == '' or
    final_creature_dict.get("Est. Max Dmg") == 'Unknown' or
    final_creature_dict.get("Est. Max Dmg") == 'Unknown.'):
    final_creature_dict["Est. Max Dmg"] = None

  #print(f"MAXDMG burster 3 cleaning is: {final_creature_dict.get('Est. Max Dmg')}")
  maxdmg_str = ''
  if(final_creature_dict.get("Est. Max Dmg") is not None and final_creature_dict.get("Est. Max Dmg") is not "Unknown"):
    for char in final_creature_dict.get("Est. Max Dmg"):
      if char.isdigit():
        maxdmg_str += char
    final_creature_dict["Est. Max Dmg"] = maxdmg_str

  if(creature_name == "Zevelon Duskbringer"):
    final_creature_dict["Est. Max Dmg"] = 1000

  if(final_creature_dict.get("Est. Max Dmg") == ''):
    final_creature_dict["Est. Max Dmg"] = None
  #print(f"MAXDMG burster 4 cleaning is: {final_creature_dict.get('Est. Max Dmg')}")
  ################ CLEAN MAX DMG NUMBERS ################ 

  ################ CLEAN CONVINCE AND SUMMON NUMBERS ################ 
  if("mana" in final_creature_dict.get("Convince")):
    #print(f"----------------- MANA CONVINCE: {final_creature_dict.get('Convince')}")
    final_creature_dict["Convince"] = final_creature_dict.get("Convince").split(" ")[0]
  
  if("mana" in final_creature_dict.get("Summon")):
    #print(f"----------------- MANA SUMMON: {final_creature_dict.get('Summon')}")
    final_creature_dict["Summon"] = final_creature_dict.get("Summon").split(" ")[0]
  ################ CLEAN CONVINCE AND SUMMON NUMBERS ################ 

  ################ CLEAN HEALTH NUMBERS ################
  if(final_creature_dict.get("Health") == "Unknown." or final_creature_dict.get("Health") == "Unknown"):
    final_creature_dict["Health"] = None

  clean_health_str = ''
  if(final_creature_dict.get("Health") is not None):
    for char in final_creature_dict.get("Health"):
      #print(char)
      if char.isdigit():
        clean_health_str += char
    final_creature_dict["Health"] = clean_health_str

  if(final_creature_dict.get("Health") == '?' or
  final_creature_dict.get("Health") == '' or
  final_creature_dict.get("Health") == 'Unknown' or
  final_creature_dict.get("Health") == 'Unknown.'):
    final_creature_dict["Health"] = None
  ################ CLEAN HEALTH NUMBERS ################

  #print(f"------------- THIS is the maxdmg value after all the conversions for creature: {creature_name} -- {final_creature_dict.get('Est. Max Dmg')} ")
  new_creature = Webscraped_Creature(
    creature_name,
    final_creature_dict.get("Health"),
    final_creature_dict.get("Experience"),
    final_creature_dict.get("Speed"),
    final_creature_dict.get("Armor"),
    final_creature_dict.get("Est. Max Dmg"),
    final_creature_dict.get("Summon"),
    final_creature_dict.get("Convince"),
    final_creature_dict.get("Illusionable"),
    final_creature_dict.get("Pushable"),
    final_creature_dict.get("Pushes"),
    final_creature_dict.get("Kills to Unlock"),
    final_creature_dict.get("Sense Invis"),
    None, None, None, None, None, None, None, None
  )



  
  ################ GET RESISTANCE FOR CREATURE ################
  results = soup.find("div", {"id": "creature-resistance-d"}) # Find div by id
  for resistance in results:
    data = resistance.get_text()
    data = data.strip()
    data = data.split(" ")
    # Clean prysical resistance numbers
    if(len(data) > 1):
      test_data_1 = data[1].split("%")
    if(data[0] == "Physical"): new_creature.dmgfromphysical = test_data_1[0]
    elif(data[0] == "Death"): new_creature.dmgfromdeath = test_data_1[0]
    elif(data[0] == "Holy"): new_creature.dmgfromholy = test_data_1[0]
    elif(data[0] == "Ice"): new_creature.dmgfromice = test_data_1[0]
    elif(data[0] == "Fire"): new_creature.dmgfromfire = test_data_1[0]
    elif(data[0] == "Energy"): new_creature.dmgfromenergy = test_data_1[0]
    elif(data[0] == "Earth"): new_creature.dmgfromearth = test_data_1[0]
    else: continue #print("This is what went wrong with the data: ", data)

  ################ GET LOOT LIST FROM CREATURE ################
  results = soup.find("div", {"id": "loot_perc_loot"}) # Find div by id
  loot_list = []
  loot_list = results.get_text().split("\n")
  new_creature.listofloot = ",".join(loot_list) # Get loot as string instead of list
  #new_creature.listofloot = loot_list
  #print("loot_list:", loot_list)

  #print(vars(new_creature))
  return new_creature
