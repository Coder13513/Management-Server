from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager)
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, timedelta
import jwt
from package.models import Package
from utils.models import BaseAbstractModel
from django.conf import settings
from fernet_fields import EncryptedTextField
from utils.managers import CustomQuerySet

class EmailField(models.EmailField):
    def get_prep_value(self, value):
        value = super(EmailField, self).get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value

class UserManager(BaseUserManager):

    def create_user(
        self,
        email=None,
        password=None,
        role='VI'
    ):

        # if not first_name:
        #     raise TypeError('Users must have a first name.')

        # if not last_name:
        #     raise TypeError('Users must have a last name.')

        if not email:
            raise TypeError('Users must have an email address.')

        if not password:
            raise TypeError('Users must have a password.')

        user = self.model(
            # first_name=first_name,
            # last_name=last_name,
            email=self.normalize_email(email),
            username=self.normalize_email(email))
        user.set_password(password),
        user.role = role,
        user.save()
        return user

    def create_superuser(
        self, email=None, password=None, username=None
    ):
        # if not first_name:
        #     raise TypeError('Superusers must have a first name.')

        # if not last_name:
        #     raise TypeError('Superusers must have a last name.')

        if not email:
            raise TypeError('Superusers must have an email address.')

        if not password:
            raise TypeError('Superusers must have a password.')

        user = self.model(
            # first_name=first_name, last_name=last_name,
            email=self.normalize_email(email), username=self.normalize_email(email), role='admin')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.set_password(password)
        user.save()

class User(AbstractUser, BaseAbstractModel):
    """ Here we will define the user modal """

    USER_ROLES = (
        ('AD', 'admin'),
        ('CA', 'client_admin'),
        ('VI', 'viewer'),
    )

    # username = models.CharField(
    #     null=True, blank=True, max_length=100, unique=True)
    email = EmailField(unique=True)
    role = models.CharField(
        verbose_name='user role', max_length=20, choices=USER_ROLES,
        default='VI'
    )
    #acct_expiry_date=models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    # USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    @property
    def get_email(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):

        ts = datetime.now()

        token = jwt.encode({
            'id': self.pk,
            'email': self.get_email,
            'ts': int(ts.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class BlackList(BaseAbstractModel):

    """ This class defines black list model.
    Tokens of logged out users are stored here. """

    token = models.CharField(max_length=200, unique=True)

    @staticmethod
    def delete_tokens_older_than_a_day():
        """
        This method deletes tokens older than one day
        """
        past_24 = datetime.now() - timedelta(hours=24)

        BlackList.objects.filter(created_at__lt=past_24).delete()

class UserDevices(BaseAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_name = models.CharField(default='Mobile', max_length=100)
    token = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.user}\'s Device'

class UserProfile(BaseAbstractModel):
    """This class defines a Profile model for all Users"""

    QUESTION_CHOICES = (
        ('What is the name of your favorite childhood friend',
         'What is the name of your favorite childhood friend'),
        ('What was your childhood nickname',
         'What was your childhood nickname'),
        ('In what city or town did your mother and father meet',
         'In what city or town did your mother and father meet')
    )

    readonly_fields = ['lapsed_recording_time']

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    phone = models.CharField(max_length=17, null=True, blank=False)
    image = models.URLField(null=True, blank=True)
    parental_lock = models.IntegerField(default=6666)
    recording_time = models.IntegerField(default=30)
    lapsed_recording_time = models.IntegerField(default=0)
    security_question = models.CharField(
        max_length=255, null=True, blank=False, choices=QUESTION_CHOICES)
    security_answer = EncryptedTextField(null=True)
    #subscription_package = models.ForeignKey(SubscriptionPackage, models.SET_NULL, blank=True, null=True)
    objects = models.Manager()
    active_objects = CustomQuerySet.as_manager()

    def __str__(self):
        return f'{self.user}\'s Profile'
