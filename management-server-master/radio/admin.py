from django.contrib import admin

# Register your models here.
from radio.models import RadioCategory, RadioChannel

admin.site.register(RadioCategory)
admin.site.register(RadioChannel)
