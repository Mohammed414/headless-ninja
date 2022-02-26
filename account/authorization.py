from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from jose import jwt, JWTError
from ninja.security import HttpBearer

User = get_user_model()

TIME_DELTA = timedelta(days=120)


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user_pk = payload.get('pk')
            if user_pk is None:
                return None
        except JWTError:
            return None
        if user_pk:
            return user_pk


def get_tokens_for_user(user):
    token = jwt.encode({'pk': str(user.pk)}, key=settings.SECRET_KEY, algorithm='HS256')
    return {
        'access': str(token),
    }
