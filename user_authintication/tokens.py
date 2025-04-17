from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return super()._make_hash_value(user, timestamp)
    

account_activation_token = AccountActivationTokenGenerator()