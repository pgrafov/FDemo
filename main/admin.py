from django.contrib import admin

from main.models import Url, Word


class WordAdmin(admin.ModelAdmin):
    list_display = ['title', 'assigned']


class UrlAdmin(admin.ModelAdmin):
    list_display = ['link', 'created']

admin.site.register(Word, WordAdmin)
admin.site.register(Url, UrlAdmin)
