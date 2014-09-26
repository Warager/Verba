from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'verba.word_stats.views.input_form'),
    url(r'^process$', 'verba.word_stats.views.process'),
    url(r'^accounts/login$', 'verba.word_stats.views.login'),
    url(r'^accounts/logout$', 'verba.word_stats.views.logout'),
    url(r'^accounts/signup$', 'verba.word_stats.views.signup'),
    url(r'^process/add_word$', 'verba.word_stats.views.add_word'),
    url(r'^process/rem_word$', 'verba.word_stats.views.rem_word'),
    url(r'^my_dictionary', 'verba.word_stats.views.my_dictionary'),

    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
