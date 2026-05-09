from core.models import GlobalLock


from django.db import DatabaseError, OperationalError

from core.globalLock.exceptions import LockAcquisitionError, LockCreationError, LockNotFoundError




class GlobalLockService:

    @staticmethod
    def acquire(name: str):
        try:
            return GlobalLock.objects.select_for_update().get(name=name)

        except GlobalLock.DoesNotExist:
            raise LockNotFoundError(name)

        except (OperationalError, DatabaseError) as e:
            raise LockAcquisitionError(str(e)) from e

        except Exception as e:
            raise LockAcquisitionError("Unexpected error") from e


    @staticmethod
    def create(name: str):
        try:
            return GlobalLock.objects.get_or_create(name=name)[0]
        except Exception as e:
            raise LockCreationError(str(e)) from e