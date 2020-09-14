from django.contrib import admin

# Register your models here.
from liveTv.models import Categories, Channels

admin.site.register(Categories)
admin.site.register(Channels)
