from django.conf.urls import patterns, include, url
from django.contrib import admin

from scrum.views import WhiteBoardView



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', WhiteBoardView.as_view(), name='whiteboard'),
    # url(r'^agile_board/', include('agile_board.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
