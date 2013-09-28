from django.conf.urls import patterns, include, url
from django.contrib import admin

from scrum.views import WhiteBoardView, add_story, add_task
from scrum.views import SprintView



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    

    url(r'^sprint/$', SprintView.as_view(), name='sprint'),
    url(r'^project/(?P<pk>[0-9]+)/$', WhiteBoardView.as_view(), name='whiteboard'),
    url(r'^project/[0-9]+/story/add/$', add_story, name='whiteboard'),
    url(r'^project/[0-9]+/task/add/$', add_task, name='whiteboard'),

    # url(r'^agile_board/', include('agile_board.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


)
