#pokedex/views.py
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.http import HttpResponseRedirect, Http404, HttpRequest
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, render_to_response
from django.forms import ModelForm
from django.db.models import Q
from collections import namedtuple
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
#from django.contrib.auth.decorators import user_passes_test
from braces.views import UserPassesTestMixin

from .models import Sample, Project, User_Project
from .forms import SampleForm, SamplePhotoForm

#User Project Authentication

#REDIRECT_UNAUTHORIZED_USER = '/unauthorized/'

#Breadcrumbs
	
breadcrumb = namedtuple('breadcrumb', ('name', 'url'))

class BreadcrumbsMixin():
    """Provides context information to allow the template to render a
    breadcrumb navigation trail.
    """
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            trail = self.breadcrumbs()
        except AttributeError as e:
            trail = []
            raise
        new_trail = []
        for step in trail:
            try:
                new_trail.append(breadcrumb(*step))
                # Reverse the urls if possible
            except TypeError:
                url = reverse(step)
                name = step.replace('_', ' ').title()
                new_trail.append(breadcrumb(name, url))
        context['breadcrumbs'] = new_trail
        return context

    def breadcrumbs(self):
        msg = "Please override the 'breadcrumbs()' method of {}"
        raise NotImplementedError(msg.format(self.__class__))

# Breadcrumbs definitions
def inventory_breadcrumb():
    return breadcrumb('Home', reverse_lazy('home'))

def sample_breadcrumbs(sample):
    return [
        #inventory_breadcrumb(),
        breadcrumb(
            sample.sample_number,
            reverse('sample_detail', kwargs={'id': sample.id})
        )
    ]

def project_breadcrumbs(project):
	breadcrumbs = [
		#inventory_breadcrumb(),
		breadcrumb(
			project.name,
			reverse('samples_by_projects', kwargs={'id': project.id})
		)
	]
	return breadcrumbs

class Main(ListView):
	template_name = 'home.html'
	model = Project
	context_object_name = 'project'

	def breadcrumbs(self):
		breadcrumbs = [inventory_breadcrumb()]
		return breadcrumbs

	def get_context_data(self, *args, **kwargs):
		context = super(Main, self).get_context_data(*args, **kwargs)
		return context

class SampleListView(BreadcrumbsMixin, UserPassesTestMixin, DetailView):
	"""View that shows all Samples currently under the specified Project"""
	
	template_name = 'sample_list.html'
	model = Project
	context_object_name = 'project'
	login_url = '/unauthorized/'
	redirect_field_name = ''
		
	def breadcrumbs(self):
		return project_breadcrumbs(self.object)

	def test_func(self, user, *args, **kwargs):
		project = self.get_object()
		user_project = User_Project.objects.all().filter(active_project = project, user_id = user)
		if user_project or user.is_superuser:
			return True
		else:
			return False
	
	def get_context_data(self, *args, **kwargs):
		#sample = self.get_object()
		project = self.get_object()
		context = super().get_context_data(*args, **kwargs)
		samples = Sample.objects.all().filter(associated_project = project)
		searchstring = self.request.GET.get('search')
		if searchstring:
			 samples = samples.filter(Q(sample_number__icontains=searchstring) | Q(name__icontains=searchstring) | Q(stripped_formula__icontains=searchstring))
		context['samples'] = samples
		context['active_search'] = self.request.GET.get('search')
		return context

	def get_object(self):
		"""Return the specific Project by its primary key ('pk')."""
        	# Find the primary key from the url
		pk = self.kwargs['id']
        	# Get the actual Project object
		project = Project.objects.get(pk=pk)
		return project

class AddSampleView(BreadcrumbsMixin, CreateView):
	template_name = 'sample_add.html'
	#success_url = reverse_lazy('home')
	form_class = SampleForm

	def breadcrumbs(self):
		breadcrumbs = [
		#inventory_breadcrumb(),
		breadcrumb('Add Sample',reverse_lazy('add_sample'))
	]
		return breadcrumbs
	
	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.save()
		#self.object = obj.save()
		return HttpResponseRedirect(obj.get_absolute_url())		

#	def post(self, request, *args, **kwargs):
#		self.object = None
#		form_class = self.form_class
#		form = self.get_form(form_class)
#		if form.is_valid():
#			form.user = self.request.user
#			form.save()
#			self.object = form
			#return render(request, template_name, {'form':form})
#			return HttpResponseRedirect(self.success_url)
#		else:
#			return self.form_invalid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(AddSampleView, self).get_context_data(*args, **kwargs)
		context.update(sample_form=SampleForm())
		return context

	def get_form_kwargs(self):
		kwargs = super(AddSampleView, self).get_form_kwargs()
		kwargs.update({"request": self.request.user})
		return kwargs

class EditSampleView(BreadcrumbsMixin, UpdateView):
	template_name = 'sample_edit.html'
	template_object_name = 'sample'
	model = Sample
	form_class = SampleForm
	
	def get_object(self):
		"""Returns the specific sample by its id"""
		id = self.kwargs['id']
		sample = Sample.objects.get(id=id)
		return sample

	def form_valid(self,form):
		obj = form.save(commit=False)
		obj.save()
		form.save_m2m()
		return HttpResponseRedirect(self.get_success_url())

	def get_form_kwargs(self):
		kwargs = super(EditSampleView, self).get_form_kwargs()
		kwargs.update({"request": self.request.user})
		return kwargs
	
	def breadcrumbs(self):
		breadcrumbs = [
			#inventory_breadcrumb(),
			#sample_breadcrumbs(self.object),
			breadcrumb(
				'Edit Sample',
				reverse(
					'edit_sample',
					kwargs={'id': self.object.id})
        	)
		]
		return sample_breadcrumbs(self.object) + breadcrumbs

class EditSamplePhotoView(BreadcrumbsMixin, UpdateView):
	template_name = 'sample_photo_edit.html'
	template_object_name = 'sample'
	model = Sample
	form_class = SamplePhotoForm
	
	def breadcrumbs(self):
		breadcrumbs = [
			#inventory_breadcrumb(),
			#sample_breadcrumbs(self.object),
			breadcrumb(
				'Edit Photo',
				reverse(
					'edit_sample_photo',
					kwargs={'id': self.object.id})
        	)
		]
		return sample_breadcrumbs(self.object) + breadcrumbs
	
	def get_object(self):
		"""Returns the specific sample by its id"""
		id = self.kwargs['id']
		sample = Sample.objects.get(id=id)
		return sample

	def form_valid(self,form):
		obj = form.save(commit=False)
		obj.save()
		return HttpResponseRedirect(self.get_success_url())
		
	
class SampleDetailView(BreadcrumbsMixin, DetailView):
	template_name = 'sample_detail.html'
	template_object_name = 'sample'
	
	def breadcrumbs(self):
		return sample_breadcrumbs(self.object)

	def get_object(self):
		"""Return the specific sample by its id"""
		id = self.kwargs['id']
		sample = Sample.objects.get(id=id)
		return sample

	def get_context_data(self, *args, **kwargs):
		sample = self.get_object()
		context = super().get_context_data(*args, **kwargs)
		return context

class UserView(DetailView):
    model = User
    #template_name = 'user_detail.html'
    context_object_name = 'target_user'

    # @login_required
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #containers = self.object.container_set.all()
        #context['container_list'] = containers.order_by('chemical', 'is_empty', 'expiration_date')
        # Compile chemical inventory statistics for this user
        #stats = {
        #    'expired_containers': expired_containers().filter(owner=self.object).count(),
        #    'total_containers': self.object.container_set.count()
        #}
        #context['stats'] = stats
        return context

def unauthorized(request):
    """A user has tried to authorize but failed, maybe not in the database."""
    context = {}
    return render(request, 'unauthorized.html', context)
