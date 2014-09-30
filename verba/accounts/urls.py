from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^accounts/login$', 'verba.word_stats.views.login'),
    url(r'^accounts/logout$', 'verba.word_stats.views.logout'),
    url(r'^accounts/signup$', 'verba.word_stats.views.signup'),

    url(r'^admin/', include(admin.site.urls)),
)
