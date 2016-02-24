#pokedex/views.py
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from .models import Sample
from .forms import SampleForm

class Main(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		return context

class SampleListView(ListView):
	"""View that shows all Samples currently in the database"""
	
	template_name = 'sample_list.html'
	model = Sample
	context_object_name = 'samples'
	
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		return context

class AddSampleView(TemplateView):
	template_name = 'sample_add.html'
	model = Sample
	form_class = SampleForm

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context.update(sample_form=SampleForm())
		return context
