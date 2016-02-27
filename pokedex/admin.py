#pokedex/admin.py

from django.contrib import admin

from .models import Sample, Project, User_Project

admin.site.register(Sample)
admin.site.register(Project)
admin.site.register(User_Project)


