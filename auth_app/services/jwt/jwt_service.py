import jwt 
from dataclasses import asdict
from auth_app.models  import User
from .JWTPayload import JWTPayload
import os



SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set! Application cannot start.")


# -----------------------------
# JWT Service
# -----------------------------
class JWTService:
    @staticmethod 
    def encode(user: User)-> str:
        payload: JWTPayload = JWTPayload.from_user(user)
        
        # this will create a JWT token following the jwt standard 
        # 0 - convert the payload and header to json then to utf-8 bytes
        # 1 - base64 encode the header and payload
        # 2 - concatenate the base64 encoded header and payload with a dot 
        # -> concatenated = base64url_encode(header) + "." + base64url_encode(payload)
        
        # 3 - create a signature = HMAC_HS256(key = base64url_decode(key), message =concatenated.encode('utf-8') )
        # 4 retrunr token = concatenated + "." + base64url_encode(signature)
        token = jwt.encode(
            payload=asdict(payload),
            key=SECRET_KEY,
            algorithm="HS256"
        )
        
        return token
    
    
    
    # let jwt error propagate to the caller to handle it
    @staticmethod
    def decode(token: str) -> JWTPayload:
        decoded_payload_dictionary = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=["HS256"]
        )
        return JWTPayload(**decoded_payload_dictionary)
    
    
        
        