from datetime import datetime, timezone
from auth_app.models import User
from django.db import OperationalError, IntegrityError
from core.exceptions.excecptions import ServerUnavailableException , InternalServerErrorException

class UserRepository:
    def find_by_email(self, email: str):
        try:
            user= User.objects.get(email=email)
            return user
        except OperationalError as e:
            raise ServerUnavailableException("Database connection failed.", cause=e)
        except User.DoesNotExist as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException("An unknown error occurred while fetching user by email.", cause=e)
        
    def find_by_id(self, user_id: int):
        try:
            user = User.objects.get(id=user_id)
            return user
        except OperationalError as e:
            raise ServerUnavailableException("Database connection failed.", cause=e)
        except User.DoesNotExist as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException("An unknown error occurred while fetching user by ID.", cause=e)

    def update_last_login_at(self, user: User):
        try:
            user.last_login_at = datetime.now(timezone.utc)
            user.save()
        except OperationalError as  e:
            raise ServerUnavailableException("Database connection failed.", cause=e)
        except Exception as e:
            raise InternalServerErrorException("An unknown error occurred while updating user last login time.", cause=e)

        
        

# --- SINGLETON ---
user_repository = UserRepository()