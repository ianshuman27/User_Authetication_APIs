from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta
from django.utils import timezone
from django.conf import settings



#this return left time
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    print(token.created)
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time

# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)

def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user = token.user)
    return is_expired, token

