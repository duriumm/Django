from django.db import models
from django.db.models import TextField, JSONField, Model

class Creature(models.Model):
  name = models.CharField(max_length=50, unique=True)
  health = models.IntegerField(default=None, null=True)
  experience = models.IntegerField(default=None, null=True)
  speed = models.IntegerField(default=None, null=True)
  armor = models.IntegerField(default=None, null=True)
  maxdmg = models.IntegerField(default=None, null=True)
  summon = models.CharField(max_length=50, default=None, null=True)
  convince = models.CharField(max_length=50, default=None, null=True)
  illusionable = models.CharField(max_length=50, default=None, null=True)
  pushable = models.CharField(max_length=50, default=None, null=True)
  pushes = models.CharField(max_length=50, default=None, null=True)
  killstounlock = models.IntegerField(default=None, null=True)
  senseinvis = models.CharField(max_length=50, default=None, null=True)
  dmgfromphysical = models.IntegerField(default=None, null=True)
  dmgfromdeath = models.IntegerField(default=None, null=True)
  dmgfromholy = models.IntegerField(default=None, null=True)
  dmgfromice = models.IntegerField(default=None, null=True)
  dmgfromfire = models.IntegerField(default=None, null=True)
  dmgfromenergy = models.IntegerField(default=None, null=True)
  dmgfromearth = models.IntegerField(default=None, null=True)
  listofloot = models.CharField(max_length=5000, default=None, null=True)

  def __str__(self):
      return f"Name: {self.name}, Health: {self.health}, Experience: {self.experience}, Speed: {self.speed}, Loot items: {self.items}"
