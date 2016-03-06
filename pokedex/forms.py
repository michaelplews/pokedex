#pokedex/forms.py
import datetime

from django import forms

from . import models

class DateInput(forms.widgets.DateInput):
    """Widget that Renders as html5 <input type="date">"""
    # Suggestion taken from https://code.djangoproject.com/ticket/21470
    input_type = 'date'
    format_key = 'DATE_INPUT_FORMATS'

class SampleForm(forms.ModelForm):
	scope_prefix = 'sample'
	form_name = 'sample_form'
	required_css_class = 'required'

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

	analysis_XRD = forms.BooleanField(label='XRD', required=False)
	analysis_EC = forms.BooleanField(label='EChem', required=False)
	analysis_TEM = forms.BooleanField(label='TEM', required=False)
	analysis_TGA = forms.BooleanField(label='TGA', required=False)
	analysis_XAS = forms.BooleanField(label='XAS', required=False)

	def __init__(self, *args, **kwargs):
		super(SampleForm, self).__init__(*args, **kwargs)

		for key in self.fields:
			pass

	class Meta:
		model = models.Sample
		fields = ['sample_number', 'name', 'formula', 'experiment_medium', 'experiment_atmosphere','experiment_variable', 'experiment_time', 'experiment_equation', 'start_date','end_date', 'comment','analysis_XRD', 'file_XRD', 'analysis_EC', 'analysis_TEM', 'analysis_TGA', 'analysis_XAS', 'associated_project']
