from django.conf.urls import patterns, include, url
from django.contrib import admin

from scrum.views import add_story, update_story, add_task, update_task, add_project, login, logout, update_project, WhiteBoardView
from scrum.views import SprintView



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    

    url(r'^sprint/(?P<pk>[0-9]+)/$', SprintView.as_view(), name='sprint'),
    url(r'^project/(?P<pk>[0-9]+)/$', WhiteBoardView.as_view(), name='project'),
    url(r'^project/(?P<pk_project>[0-9]+)/update/$', update_project, name='updateproject'),
    url(r'^project/(?P<pk_project>[0-9]+)/story/add/$', add_story, name='addstory'),
    url(r'^project/(?P<pk_project>[0-9]+)/story/(?P<pk_story>[0-9]+)/$', update_story, name='updatestory'),
    url(r'^project/(?P<pk_project>[0-9]+)/task/add/$', add_task, name='addtask'),
    url(r'^project/(?P<pk_project>[0-9]+)/task/(?P<pk_task>[0-9]+)/$', update_task, name='updatetask'),
    url(r'^project/add/$', add_project, name='addproject'),
    
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),


    # url(r'^agile_board/', include('agile_board.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


)
