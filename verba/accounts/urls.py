from django.conf.urls import patterns, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^login$', 'verba.accounts.views.login'),
    url(r'^logout$', 'verba.accounts.views.logout'),
    url(r'^signup$', 'verba.accounts.views.signup'),

)
