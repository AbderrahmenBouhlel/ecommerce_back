from django.db import IntegrityError, OperationalError, transaction

from auth_app.models import User
from auth_app.services.jwt import JWTService
from core.services.password import PasswordService
from core.exceptions.excecptions import (
    ServerUnavailableException,
    InternalServerErrorException,
)
from auth_app.apis.signup.dtos import SignupResponseDTO
from auth_app.apis.signup.exceptions import (
    EmailAlreadyExistsException,
    WeakPasswordException,
    InvalidEmailException
)
from auth_app.apis.signup.service.auth_validation import SignupValidationService


class SignupService:
    def __init__(self):
        self.validation_service = SignupValidationService()


    @transaction.atomic
    def execute(self, email: str, password: str, name: str) -> SignupResponseDTO:
        """
        Creates the account immediately and returns a JWT token.
        """
        try:
            # 1) Business validation
            self.validation_service.validate(email=email, password=password)
            

            # 2) Hash password
            password_hash = PasswordService.hash_password(password)

            # 3) Create user inside a transaction
           
            user: User = self._create_user(
                email=email,
                name=name,
                password_hash=password_hash,
                role="CUSTOMER",
                is_active=True,
            )

            # 4) Generate token
            token: str = JWTService.encode(user)


            # 5) Build response
            responseDto = SignupResponseDTO(
                token=token,
                id=str(user.id),
                email=user.email,
                name=user.name,
                role=user.role,
            )
            
            return responseDto

        except (
            WeakPasswordException,
            InvalidEmailException,
            EmailAlreadyExistsException,
        ) as e:
            raise
        except (ServerUnavailableException | InternalServerErrorException):
            raise
        except Exception as e:
            raise InternalServerErrorException(
                message="An unknown error occurred while creating the account.",
                cause=e,
            )
            
            
    def _create_user(self, email: str, name: str, password_hash: str, role: str, is_active: bool) -> User:
        try:
            user = User.objects.create(
                email=email,
                name=name,
                password_hash=password_hash,
                role=role,
                is_active=is_active,
            )
            return user
        except IntegrityError as e:
            raise EmailAlreadyExistsException("A user with this email already exists.", cause=e)
        except OperationalError as e:
            raise ServerUnavailableException("Database connection failed.", cause=e)
        except Exception as e:
            raise InternalServerErrorException("An unknown error occurred while creating a new user.", cause=e)