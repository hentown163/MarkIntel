"""Authentication API Endpoints"""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.aws_ad_auth import get_ad_auth_service
from app.core.auth_middleware import get_current_user, TokenData


router = APIRouter(prefix="/api/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response model"""
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    """User information response"""
    username: str
    email: str
    name: str
    department: Optional[str] = None


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Authenticate user with AWS Active Directory and return JWT token
    
    Args:
        request: Login credentials (username and password)
        
    Returns:
        JWT access token and user information
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        ad_service = get_ad_auth_service()
        
        # Authenticate user against AWS AD
        user_info = ad_service.authenticate_user(
            username=request.username,
            password=request.password
        )
        
        if user_info is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create JWT token
        access_token = ad_service.create_user_token(user_info)
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user={
                "username": user_info["username"],
                "email": user_info["email"],
                "name": user_info["display_name"],
                "department": user_info.get("department")
            }
        )
        
    except ValueError as e:
        # Configuration error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        # Unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: TokenData = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Args:
        current_user: Current user from JWT token (injected by dependency)
        
    Returns:
        Current user information
    """
    return UserResponse(
        username=current_user.username,
        email=current_user.email,
        name=current_user.name,
        department=current_user.department
    )


@router.post("/logout")
async def logout():
    """
    Logout endpoint (client should discard token)
    
    Returns:
        Success message
    """
    return {"message": "Successfully logged out. Please discard your token."}


@router.get("/health")
async def auth_health_check():
    """
    Health check for authentication service
    
    Returns:
        Service status
    """
    try:
        ad_service = get_ad_auth_service()
        return {
            "status": "healthy",
            "ad_configured": ad_service.ad_server is not None
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
