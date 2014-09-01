from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'hello.word_stats.views.input_form'),
    url(r'^process$', 'hello.word_stats.views.process'),
    url(r'^accounts/login$', 'hello.word_stats.views.accounts'),
    url(r'^accounts/logout$', 'hello.word_stats.views.logout'),
    url(r'^accounts/signup$', 'hello.word_stats.views.signup'),
    url(r'^process/add_word$', 'hello.word_stats.views.add_word'),
    url(r'^process/rem_word$', 'hello.word_stats.views.rem_word'),
    url(r'^my_dictionary', 'hello.word_stats.views.my_dictionary'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
