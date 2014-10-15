from django.conf.urls import patterns, include, url

from django.contrib import admin
from verba import accounts
from verba.accounts import urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'verba.word_stats.views.input_form'),
    url(r'^process$', 'verba.word_stats.views.process'),
    url(r'^process/add_word$', 'verba.word_stats.views.add_word'),
    url(r'^process/rem_word$', 'verba.word_stats.views.rem_word'),
    url(r'^my_dictionary', 'verba.word_stats.views.my_dictionary'),
    url(r'^about$', 'verba.word_stats.views.about'),
    url(r'^contact$', 'verba.word_stats.views.contact'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(accounts.urls)),
)
