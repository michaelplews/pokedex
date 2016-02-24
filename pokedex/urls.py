from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from . import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$',
		views.Main.as_view(), 
		name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^samples/$',
		views.SampleListView.as_view(),
		name='sample_list'),
	url(r'^add/$',
		views.AddSampleView.as_view(),
		name='add_sample'),
	url(r'^admin/', include(admin.site.urls)),
)
