from django.core.exceptions import (
    ValidationError,
)
from django.utils.translation import gettext as _
import re

class NumericPasswordValidator:
    """
    Validate whether the password is alphanumeric.
    """
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("This password is entirely numeric."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Your password can't be entirely numeric.")

class RegexPasswordValidator:
    """
    Validate whether the password contains 
    """
    def validate(self, password, user=None):
        passwordRegex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$") #Password must contain minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:
        if not passwordRegex.match(password):
            raise ValidationError("Le mot de passe doit contenir au minimum 8 caractères, une lettre minuscule, une lettre majuscule, un chiffre et un caractère spécial.")

    def get_help_text(self):
        return _("Your password can't be entirely numeric.")   #