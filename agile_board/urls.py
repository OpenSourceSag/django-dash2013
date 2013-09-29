from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings

from scrum.views import *


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', login_required(ProjectListView.as_view()), name='projectlist'),
    url(r'^sprint/(?P<pk>[0-9]+)/$', login_required(SprintView.as_view()), name='sprint'),
    url(r'^sprint/(?P<pk>[0-9]+)/close/$', close_sprint, name='closesprint'),
    url(r'^project/(?P<pk>[0-9]+)/$', login_required(WhiteBoardView.as_view()), name='project'),
    url(r'^project/(?P<pk_project>[0-9]+)/update/$', login_required(update_project), name='updateproject'),
    url(r'^project/(?P<pk_project>[0-9]+)/story/add/$', login_required(add_story), name='addstory'),
    url(r'^project/[0-9]+/story/(?P<pk_story>[0-9]+)/$', login_required(update_story), name='updatestory'),
    url(r'^project/(?P<pk_project>[0-9]+)/task/add/$', login_required(add_task), name='addtask'),
    url(r'^project/[0-9]+/task/(?P<pk_task>[0-9]+)/$', login_required(update_task), name='updatetask'),
    url(r'^project/[0-9]+/sprint-task/add/$', login_required(add_sprint_task), name='updatetask'),
    url(r'^project/(?P<pk>[0-9]+)/sprint/add/$', login_required(add_sprint), name='sprintadd'),
    url(r'^project/add/$', login_required(add_project), name='addproject'),
    url(r'^task/(?P<pk_task>[0-9]+)/update-status/$', login_required(update_task), name='updatetaskstatus'),

    url(r'^login/?$', 'django.contrib.auth.views.login', {'template_name': 'scrum/registration/login.html', }, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'scrum/registration/logged_out.html', }, name='logout'),
)

urlpatterns += patterns('',
    (r'^static/(.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),
)
