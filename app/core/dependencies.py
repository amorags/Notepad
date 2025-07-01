from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from app.db.session import get_db
from app.core.security import decode_access_token
from app.crud.user import get_user_by_email

# Security scheme for Bearer token
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Dependency to get the current authenticated user from JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Extract token from credentials
        token = credentials.credentials
        
        # Decode the JWT token
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception
        
        # Extract user email from token payload
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user