#pokedex/views.py
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from .models import Sample, Project, User_Project
from .forms import SampleForm

class Main(ListView):
	template_name = 'home.html'
	model = Project
	context_object_name = 'project'

	def get_context_data(self, *args, **kwargs):
		context = super(Main, self).get_context_data(*args, **kwargs)
		return context

class SampleListView(DetailView):
	"""View that shows all Samples currently in the database"""
	
	template_name = 'sample_list.html'
	model = Project
	context_object_name = 'project'
		

	def get_context_data(self, *args, **kwargs):
		#sample = self.get_object()
		project = self.get_object()
		context = super(SampleListView, self).get_context_data(*args, **kwargs)
		context['samples'] = Sample.objects.all().filter(associated_project = project)
		return context

	def get_object(self):
		"""Return the specific chemical by its primary key ('pk')."""
        	# Find the primary key from the url
		pk = self.kwargs['id']
        	# Get the actual Chemical object
		project = Project.objects.get(pk=pk)
		return project	

	def get_queryset(self, *args, **kwargs):
		queryset = Sample.objects.all()
		project = self.get_object()
		if project is not None:
			#queryset = queryset.filter(associated_project==project)
			return queryset
		else:	
			return queryset

class AddSampleView(TemplateView):
	template_name = 'sample_add.html'
	model = Sample
	form_class = SampleForm

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context.update(sample_form=SampleForm())
		return context
