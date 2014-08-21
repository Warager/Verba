from django.contrib import admin
from hello.word_stats.models import UserDictionary


class UserDictionaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'word']
admin.site.register(UserDictionary,UserDictionaryAdmin)
