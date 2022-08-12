from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class AccountActivationToken(PasswordResetTokenGenerator):
    # PasswordResetTokenGenerator 의 내장 함수를 불러온다.
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(user.is_active)

account_activation_token = AccountActivationToken()