from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

"""
Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019

Forms/templates: N/A
Methods: N/A
Inputs: N/A
Output: hash of the user.pk, timestampt, is_active and last_login

This Helper class is used to manage the intricacies of the token used in the user activate, register and verification
token when called.

"""
class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk)+text_type(timestamp)+text_type(user.is_active)+text_type(user.last_login))

token_generator = AppTokenGenerator()
