from django.db import models
from authentication.models import User
from utils.models import BaseAbstractModel

# Create your models here.
class DeviceType(BaseAbstractModel):
    device_type = models.CharField(max_length=200, unique=True)
    device_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.device_type}'

class SubscriptionPackage(BaseAbstractModel):
    package_name = models.CharField(max_length=200)
    package_description = models.TextField()

    def __str__(self):
        return f'{self.package_name}'
    
class SubscriptionPackageDevices(BaseAbstractModel):
    package = models.ForeignKey(SubscriptionPackage, on_delete=models.CASCADE)
    device = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    connections = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.package}_{self.device}'

    class Meta:
        unique_together = ('package','device',)

class UserSubscriptionPackage(BaseAbstractModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    package = models.ForeignKey(SubscriptionPackage, on_delete=models.CASCADE)     

    def __str__(self):
        return f'{self.user}\'s package'    

class IndividualSubscriptionDevices(BaseAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    connections = models.IntegerField(default=1)   

    def __str__(self):
        return f'{self.user}\'s individual device subscription'

    class Meta:
        unique_together = ('user','device',)

class UserActiveSession(BaseAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=30, unique=True)
    device_model = models.CharField(max_length=50)
    location = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
       return f'{self.user}\'s {self.device}'    
