#pokedex/admin.py

from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import Sample, Project, User_Project

class SampleAdmin(ImageCroppingMixin, admin.ModelAdmin):
	pass

admin.site.register(Sample, SampleAdmin)
admin.site.register(Project)
admin.site.register(User_Project)


