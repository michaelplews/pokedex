from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf import settings
from . import views

urlpatterns = patterns('',
    # Examples:
    	url(r'^$',
		views.Main.as_view(), 
		name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^project/(?P<id>[0-9]+)/$',
		views.SampleListView.as_view(),
		name='samples_by_projects'),
	url(r'^add/$',
		views.AddSampleView.as_view(),
		name='add_sample'),
	url(r'^sample/(?P<id>[0-9]+)/$',
		views.SampleDetailView.as_view(),
		name='sample_detail'),
	url(r'^edit/(?P<id>[0-9]+)/$',
		views.EditSampleView.as_view(),
		name='edit_sample'),
	url(r'^edit_photo/(?P<id>[0-9]+)/$',
		views.EditSamplePhotoView.as_view(),
		name='edit_sample_photo'),	
	url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.MEDIA_ROOT}))
