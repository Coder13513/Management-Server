from django.contrib import admin
from subscription.models import DeviceType, SubscriptionPackage, SubscriptionPackageDevices, IndividualSubscriptionDevices
from subscription.models import UserSubscriptionPackage, UserActiveSession
# Register your models here.
admin.site.register(DeviceType)
admin.site.register(SubscriptionPackage)
admin.site.register(SubscriptionPackageDevices)
admin.site.register(IndividualSubscriptionDevices)
admin.site.register(UserSubscriptionPackage)
admin.site.register(UserActiveSession)
