from django.contrib import admin

# Register your models here.

from package.models import Package

admin.site.register(Package)
