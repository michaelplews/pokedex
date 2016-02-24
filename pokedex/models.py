#pokedex/models.py
import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models import signals

class Sample(models.Model):
	"""A Sample refers to the resulting compound of a specific experiment
	"""
	sample_id = models.CharField(max_length=10, db_index=True)
	name = models.CharField(max_length=200, db_index=True)
	formula = models.CharField(max_length=50, db_index=True, blank=True)
	stripped_formula = models.CharField(max_length=50, db_index=True, blank=True)

	AVAILABLE_MEDIUMS = [
		(0, 'Ballmill'), 
		(1, 'Tube: Borosilicate'),
		(2, 'Tube: Quartz'), 
		(3, 'Tube: Alumina'),
	]
	AVAILABLE_ATMOSPHERES = [
		(0, 'Argon'), 
		(1, '5%H2:95%N2'), 
		(2, 'Oxygen'),
		(3, 'Nitrogen'), 
		(4, 'Air'),
	]

	experiment_medium = models.IntegerField(choices=AVAILABLE_MEDIUMS)
	experiment_atmosphere = models.IntegerField(choices=AVAILABLE_ATMOSPHERES)
	experiment_temperature = models.FloatField()
	experiment_equation = models.CharField(max_length=200)

	start_date = models.DateField(null=True, default=datetime.date.today)
	end_date = models.DateField(null=True, default=datetime.date.today)

	user = models.ForeignKey(User, blank=True, null=True)

	class Meta:
		ordering = ['sample_id']

	def __str__(self):
		return "{sample_id} ({formula})".format(name=self.name, formula=self.stripped_formula)

@receiver(signals.pre_save, sender=Sample)
def strip_formula(sender, instance, raw, using, update_fields, *args, **kwargs):
	"""Strips the formula supplied to remove underscores and carrots, saves it as the stripped_formula field. Used for formula searching."""
	instance.stripped_formula = instance.formula.replace("_","").replace("^","")

class Medium(models.Model):
	"""The Medium describes the vessel where the reaction was completed."""
	name = models.CharField(max_length=50)
	
class Gas(models.Model):
	"""The Gas describes the atmosphere the reaction was done in."""
	name = models.CharField(max_length=50) 