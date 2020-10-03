from django.contrib import admin

from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first', 'last', 'speaks', 'learns', 'photo')
    list_editable = ('first', 'last', 'speaks', 'learns')

admin.site.register(Profile, ProfileAdmin)

