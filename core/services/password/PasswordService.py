import bcrypt
import os




class PasswordService:
    @staticmethod
    def hash_password(password: str) -> bytes:
        #1- encode the password to bytes
        encoding = os.getenv("PASSWORD_ENCODING", "utf-8")
        password_bytes = password.encode(encoding)
        
        #2- genrate randow salt 
        rounds = int(os.getenv("BCRYPT_ROUNDS", 12))
        salt = bcrypt.gensalt(rounds=rounds)
        
        #3- hash the passwored with the salt
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password
    
    
    @staticmethod
    def check_password(password: str, hashed_password: bytes) -> bool:
        encoding = os.getenv("PASSWORD_ENCODING", "utf-8")
        password_bytes: bytes = password.encode(encoding)
        
        return bcrypt.checkpw(password_bytes, hashed_password)