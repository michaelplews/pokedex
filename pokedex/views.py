#pokedex/views.py
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from django.http import HttpResponseRedirect, Http404, HttpRequest
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, render_to_response
from django.forms import ModelForm

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
	"""View that shows all Samples currently in the under the specified Project"""
	
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
		"""Return the specific Project by its primary key ('pk')."""
        	# Find the primary key from the url
		pk = self.kwargs['id']
        	# Get the actual Project object
		project = Project.objects.get(pk=pk)
		return project	
	


class AddSampleView(CreateView):
	template_name = 'sample_add.html'
	#	model = Sample
	success_url = reverse_lazy('home')
	form_class = SampleForm

	def form_valid(self, form):
		if form.is_valid:
			form.save()
			#return render(request, template_name, {'form':form})
			return HttpResponseRedirect(self.success_url)
	
	def form_invalid(self, form):
		return render_to_response(self.template_name, {'form':form})
	
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context.update(sample_form=SampleForm())
		return context
