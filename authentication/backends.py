import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from authentication.models import User, UserDevices


"""JWT Authentication Configuration"""


class JWTAuthentication(authentication.BaseAuthentication):
    auth_header_prefix = 'Bearer'.lower()  # change bearer to lowercase

    def authenticate(self, request):
        """
        This method will be called everytime an endpoint is accessed.

        This method can return 'None' when we want authentication to
        fail, for example when no authentication credentials are provided.

        It can also return `(user, token)` when authentication is successful.

        If we encounter an error, we raise an `AuthenticationFailed` error.
        """
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            # if we get no authentication header, we stop the authentication
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:

            return None

        # We have to decode both the prefix and token because they are in bytes,
        # and the JWT library we use can't handly bytes.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != self.auth_header_prefix:
            # The auth header prefix should only be 'Bearer'. If otherwise,
            # don't attempt to authenticate
            return None

        # We can now attempt to authenticate after performing the above checks.
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        We will try to authenticate the token. If authentication is successful
        we return (user, token), otherwise we return an `AuthenticationFailed`
        error.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)

        except jwt.ExpiredSignatureError:
            msg = 'Your token has expired, please log in again.'
            raise exceptions.AuthenticationFailed(msg)

        except Exception as e:
            msg = str(e)
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'User matching this token was not found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'Forbidden! This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        active_session = UserDevices.objects.filter(user_id=user.id).first()
        if active_session == None:
            print("No active session")
            uDevice = UserDevices(user=user, token=token)
            uDevice.save()
        if active_session != None and active_session.token != token:
            print("Active session already exists")
            raise exceptions.AuthenticationFailed("User session is active on other device")        
        return (user, token)
