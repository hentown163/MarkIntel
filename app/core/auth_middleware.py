"""Authentication Middleware for FastAPI"""
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.auth_helpers import decode_token


# HTTP Bearer token security
security = HTTPBearer()


class TokenData:
    """Token data model"""
    def __init__(self, username: str, email: str, name: str, department: Optional[str] = None):
        self.username = username
        self.email = email
        self.name = name
        self.department = department


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Dependency to extract and validate current user from JWT token
    
    Args:
        credentials: HTTP Authorization credentials with Bearer token
        
    Returns:
        TokenData object with user information
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    
    # Decode and validate token
    payload = decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return TokenData(
        username=username,
        email=payload.get("email", ""),
        name=payload.get("name", username),
        department=payload.get("department")
    )


async def get_optional_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[TokenData]:
    """
    Optional dependency to extract user from JWT token
    Returns None if token is invalid
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        TokenData object with user information or None
    """
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
