from datetime import datetime
import jwt

class TokenHelper:
    def get_token(jwt_token):
        return jwt.decode(jwt_token, verify=False)

    def expiration(jwt_token):
        decoded = TokenHelper.get_token(jwt_token)
        exp = decoded["exp"]
        return datetime.utcfromtimestamp(exp)
    
    def is_expired(jwt_token):
        expiration = TokenHelper.expiration(jwt_token)
        return expiration < datetime.utcnow()