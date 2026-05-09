from core.exceptions.excecptions import RequestValidationException
from auth_app.repos.UserRespository import user_repository
from auth_app.models import User
from core.exceptions.excecptions import  InvalidCredentialsException 
from auth_app.apis.login.exception import AccountDisabledException
from core.services.password import PasswordService
from auth_app.services.jwt import JWTService

from auth_app.apis.login.dtos import LoginResponseDTO

class LoginService:
    
    def execute(self , email :str , password : str) -> LoginResponseDTO:
        """
        Orchestrates the login flow.

        Args:
            email (str): The user's email identifier.
            password (str): The raw password to verify.

        Returns:
            LoginResponseDTO: The successful login payload.

        Raises:
            RequestValidationException: If input fields are empty (400).
            InvalidCredentialsException: If user not found or password wrong (401).
            ServerUnavailableException: If the database connection fails (503).
            InternalServerErrorException: If an unknown  error occurs (500).
            
        """
        
      
        # 1 validate  the request
        self.assert_valid_request(email , password)
        
        # 2 find the user by email
        user: User = self.find_user_by_email(email)
        
       
        # 3 check the password
        self.assert_password_matches(password , user.password_hash)
        
        #4 check if the account is active
        self.assert_user_active_status(user)
        
        #5 generate JWT token 
        token: str = JWTService.encode(user)
        
        #6 update last login time
        user_repository.update_last_login_at(user)
        
        login_response_dto = LoginResponseDTO(
            token=token,
            id=str(user.id),
            email=user.email,
            name=user.name,
            role=user.role,
        )
        
        
        return login_response_dto
    
    
    def find_user_by_email(self , email :str) -> User:
        try :
            user: User = user_repository.find_by_email(email)
            return user
        except User.DoesNotExist as e:
            raise InvalidCredentialsException(message="user not found.", cause=e) 
        
    def assert_password_matches(self , password :str , hashed_password :bytes):
        if not PasswordService.check_password(password , hashed_password):
            raise InvalidCredentialsException(message="Invalid password.", cause=None)
        
    def assert_valid_request(self , email :str , password : str):
        if not email or not password:
            raise RequestValidationException(message="Invalid Login request.", cause=None)
        
    def assert_user_active_status(self , user :User):
        if not user.is_active:
            raise AccountDisabledException(message="Account deactivated.", cause=None)