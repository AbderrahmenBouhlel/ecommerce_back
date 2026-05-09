

import datetime
from dataclasses import dataclass
import os


try :
    JWT_TTL = int(os.getenv("JWT_TTL"))
except (TypeError, ValueError):
    raise RuntimeError("JWT_TTL is missing or invalid! It must be an integer.")

    


@dataclass
class JWTPayload:
    id: int
    role: str
    exp: int
    
    @staticmethod 
    def from_user(user):
        return JWTPayload(
            id=user.id,
            role=user.role,
            exp=int((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=JWT_TTL)).timestamp())
        )
        