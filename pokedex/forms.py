#pokedex/forms.py
import datetime

from django import forms
from image_cropping import ImageCropWidget
from braces.forms import UserKwargModelFormMixin

from . import models

class DateInput(forms.widgets.DateInput):
    """Widget that Renders as html5 <input type="date">"""
    # Suggestion taken from https://code.djangoproject.com/ticket/21470
    input_type = 'date'
    format_key = 'DATE_INPUT_FORMATS'

class SampleForm(UserKwargModelFormMixin, forms.ModelForm):
	scope_prefix = 'sample'
	form_name = 'sample_form'
	required_css_class = 'required'
	#user_project = models.Project.objects.all().filter(user_id = request.get.user)

	sample_number = forms.CharField(label='Sample ID', max_length=10, required=True)
	name = forms.CharField(max_length=200, required=True)
	formula = forms.CharField(max_length=50, required=False)

	experiment_variable = forms.FloatField(label='Variable (rpm/oC/etc.)', required=True)
	experiment_time = forms.FloatField(label='Time (h)', required=True)
	experiment_equation = forms.CharField(label='Stoichiometric Equation', max_length=200, required=False)


	start_date = forms.DateField(widget=DateInput(),
                                  required=False)
	end_date = forms.DateField(widget=DateInput(),
                                  required=False)

	associated_project = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=models.Project.objects.all(), required=True)

	def __init__(self, *args, **kwargs):
		super(SampleForm, self).__init__(*args, **kwargs)
		user_project = models.User_Project.objects.all()
		projects = models.Project.objects.all().filter(id = user_project)
		#self.fields['associated_project'].queryset = projects
		for key in self.fields:
			pass

	class Meta:
		model = models.Sample
		widget = {
			'file_photo': ImageCropWidget,
				}
		fields = [
		'sample_number', 'name', 'formula', 'experiment_medium', 			'experiment_atmosphere','experiment_variable', 'experiment_time', 			'experiment_equation', 'start_date','end_date', 'comment', 'file_photo', 'cropping', 'file_XRD', 		'file_EC', 'file_TEM', 'file_TGA', 'file_XAS','associated_project'
		]

class SamplePhotoForm(UserKwargModelFormMixin, forms.ModelForm):
	scope_prefix = 'sample'
	form_name = 'sample_photo_form'
	required_css_class = 'required'

	class Meta:
		model = models.Sample
		widget = {
			'file_photo': ImageCropWidget,
				}
		fields = [
		'file_photo', 'cropping'
		]
