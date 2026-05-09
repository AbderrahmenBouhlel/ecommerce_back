import re
from auth_app.apis.signup.exceptions import (
    InvalidEmailException,
    WeakPasswordException
)


class SignupValidationService:
    EMAIL_REGEX = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

    def assert_validate_email(self, email: str) -> None:
        if not re.match(self.EMAIL_REGEX, email):
            raise InvalidEmailException()

    def assert_validate_password(self, password: str) -> None:
        """
        Policy:
        - at least 8 chars
        - at least one letter
        - at least one number
        """
        if len(password) < 8:
            raise WeakPasswordException("Password must be at least 8 characters long and include letters and numbers.")

        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)

        if not has_letter or not has_digit:
            raise WeakPasswordException("Password must be at least 8 characters long and include letters and numbers.")


    def validate(self, email: str, password: str) -> None:
        self.assert_validate_email(email)
        self.assert_validate_password(password)
        