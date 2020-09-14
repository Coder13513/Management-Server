from django.contrib import admin

# Register your models here.

from .models import Category, Content

admin.site.register(Category)
admin.site.register(Content)
