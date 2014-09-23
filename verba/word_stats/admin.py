from django.contrib import admin
from verba.word_stats.models import UserDictionary


class UserDictionaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'word', 'created']


admin.site.register(UserDictionary, UserDictionaryAdmin)
