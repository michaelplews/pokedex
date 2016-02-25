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
	sample_number = models.CharField(max_length=10, db_index=True)
	name = models.CharField(max_length=200, db_index=True)
	formula = models.CharField(max_length=50, db_index=True, blank=True)
	stripped_formula = models.CharField(max_length=50, db_index=True, blank=True)

	AVAILABLE_MEDIUMS = [
		('Ballmill', 'Ballmill'), 
		('Tube: Borosilicate', 'Tube: Borosilicate'),
		('Tube: Quartz', 'Tube: Quartz'), 
		('Tube: Alumina', 'Tube: Alumina'),
	]
	AVAILABLE_ATMOSPHERES = [
		('Argon', 'Argon'), 
		('5%H2:95%N2', '5%H2:95%N2'), 
		('Oxygen', 'Oxygen'),
		('Nitrogen', 'Nitrogen'), 
		('Air', 'Air'),
	]

	experiment_medium = models.CharField(max_length=50, choices=AVAILABLE_MEDIUMS)
	experiment_atmosphere = models.CharField(max_length=50, choices=AVAILABLE_ATMOSPHERES)
	experiment_variable = models.FloatField(null=True, blank=True)
	experiment_time = models.FloatField()
	experiment_equation = models.CharField(max_length=200, blank=True)
	variable_units = models.CharField(max_length=5, blank=True)	

	analysis_XRD = models.BooleanField()
	analysis_EC = models.BooleanField()
	analysis_TEM = models.BooleanField()
	analysis_TGA = models.BooleanField()
	analysis_XAS = models.BooleanField()

	start_date = models.DateField(null=True, default=datetime.date.today)
	end_date = models.DateField(null=True, default=datetime.date.today)

	user = models.ForeignKey(User, blank=True, null=True)

	class Meta:
		ordering = ['sample_number']

	def __str__(self):
		return "{sample_number} ({formula})".format(sample_number=self.sample_number, formula=self.stripped_formula)

@receiver(signals.pre_save, sender=Sample)
def strip_formula(sender, instance, raw, using, update_fields, *args, **kwargs):
	"""Strips the formula supplied to remove underscores and carrots, saves it as the stripped_formula field. Used for formula searching."""
	instance.stripped_formula = instance.formula.replace("_","").replace("^","")

@receiver(signals.pre_save, sender=Sample)
def add_variable_units(sender, instance, raw, using, update_fields, *args, **kwargs):
	"""Adds the variable units of the experiment_variable field depending on the experiment_medium"""
	if 'Tube:' in instance.experiment_medium:
		instance.variable_units = '^oC'
	elif 'Ballmill' in instance.experiment_medium:
		instance.variable_units = 'rpm'
