from subscription.models import UserSubscriptionPackage, IndividualSubscriptionDevices, DeviceType
from django.core.exceptions import ObjectDoesNotExist
from subscription.models import SubscriptionPackageDevices, UserActiveSession
class SubscriptionSessionManager(object):
   
    def __init__(self):
        pass    

    def get(self, user, device_name, device_model, device_type, mac_address, location):
        session_allowed = self.check(user.id, device_type)   
        device = self.get_device(device_type) 
        if(session_allowed == True and device != None):
            new_session = UserActiveSession(user=user, device_model=device_model, device=device, mac_address=mac_address, location=location)
            new_session.save()
            return True
        return False


    def check(self, user_id, device_type): 
        device_id = self.get_device_id(device_type)
        if device_id == None:
            return False
        allowed_conn = self.get_user_allowed_connection_for_device(user_id, device_id)
        print('allowed connection ' + str(allowed_conn))
        if allowed_conn <= 0:
            return False
        active_conn = self.user_active_session_for_device(user_id, device_id)        
        print('active connection ' + str(active_conn))
        if allowed_conn <= active_conn:
            return False
        return True

    def put(self, mac_address):
        try:
            session = UserActiveSession.objects.get(mac_address=mac_address)
            session.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def get_device(self, device_type):
        try:
            device = DeviceType.objects.get(device_type=device_type)
            return device
        except ObjectDoesNotExist:
            return None
    
    def get_device_id(self, device_type):
        device = self.get_device(device_type)
        if device != None:
             return device.id
        return None

    def get_user_allowed_connection_for_device(self, user_id, device_id):
        allowed_conn = 0
        try:
            package = UserSubscriptionPackage.objects.get(user=user_id)
            print(package)
            pac_devices = SubscriptionPackageDevices.objects.filter(package=package.package).filter(device=device_id).first()
            if pac_devices != None:
                print('user sub allowed conn ' + str(pac_devices.connections));
                allowed_conn += pac_devices.connections;
        except ObjectDoesNotExist:
             print('user doesn\'t have any active subscriptions')        
        try:
            extra_priv = IndividualSubscriptionDevices.objects.filter(user=user_id).filter(device=device_id).first()
            if extra_priv != None:
                allowed_conn += extra_priv.connections
        except ObjectDoesNotExist:
            print('user doesn\'t have extra privileged subscriptions')
        return allowed_conn

    def user_active_session_for_device(self, user_id, device_id):
        try:
            sessions = UserActiveSession.objects.filter(user=user_id).filter(device=device_id)
            return sessions.count()
        except ObjectDoesNotExist:
            return 0;
