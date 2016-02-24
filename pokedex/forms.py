#pokedex/forms.py
import datetime

from django import forms
from djangular.forms import NgFormValidationMixin, NgModelFormMixin, NgModelForm, NgForm
from djangular.styling.bootstrap3.forms import Bootstrap3FormMixin

from . import models

class DateInput(forms.widgets.DateInput):
    """Widget that Renders as html5 <input type="date">"""
    # Suggestion taken from https://code.djangoproject.com/ticket/21470
    input_type = 'date'
    format_key = 'DATE_INPUT_FORMATS'

class SampleForm(forms.ModelForm):
	scope_prefix = 'sample'
	form_name = 'sample_form'

	sample_id = forms.CharField(label='Sample ID', max_length=10, required=True)
	name = forms.CharField(max_length=200, required=True)
	formula = forms.CharField(max_length=50, required=False)

	experiment_temperature = forms.FloatField(label='Temperature')
	experiment_equation = forms.CharField(label='Stoichiometric Equation', max_length=200)

	start_date = forms.DateField(widget=DateInput(),
                                  required=False)
	end_date = forms.DateField(widget=DateInput(),
                                  required=False)
	class Meta:
		model = models.Sample
		fields = ['sample_id', 'name', 'formula', 'experiment_medium', 'experiment_atmosphere',
					'experiment_temperature', 'experiment_equation', 'start_date', 'end_date']
