import bcrypt
from server.gateways.database.database import Database

class LoginService:
    def __init__(self):
        self.db = Database()
    
    def authenticate(self, email: str, password: str):
        """
        Authenticate user by checking email and password against database
        Returns user info if successful, None if failed
        """
        session = self.db.get_session()
        try:
            # Find user by email
            from server.gateways.database.schemas.User import Users
            user = session.query(Users).filter(Users.email == email).first()
            
            if not user:
                return None
            
            # Check if password matches the hash in database
            password_matches = bcrypt.checkpw(
                password.encode('utf-8'),
                user.password_hash.encode('utf-8')
            )
            
            if not password_matches:
                return None
            
            # Return user info (don't return password!)
            return {
                'user_id': user.user_id,
                'email': user.email,
                'username': user.username
            }
        finally:
            session.close()