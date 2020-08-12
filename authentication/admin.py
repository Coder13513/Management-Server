from django.contrib import admin

# Register your models here.
from authentication.models import (
    User, BlackList, UserProfile, UserDevices
)

admin.site.register(User)
admin.site.register(BlackList)
admin.site.register(UserProfile)
admin.site.register(UserDevices)
