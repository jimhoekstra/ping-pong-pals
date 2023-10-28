from django.db import models
from django.contrib.auth.models import User
import secrets


def new_sign_up_key():
    return secrets.token_urlsafe(16)


class SignupKey(models.Model):
    code = models.CharField(max_length=32, default=new_sign_up_key)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return 'Signup Key: ' + self.code[:5] + '...'
