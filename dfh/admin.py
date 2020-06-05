from django.contrib import admin

# Register your models here.
from dfh.models import *


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    """ Define admin model for custom User model with no email field """
    list_display = ('uuid', 'p', 'g', 'key', 'email')