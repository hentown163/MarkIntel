import pytest
from datetime import datetime, timedelta
from jose import jwt
from app.utils.auth_helpers import create_access_token, decode_token
from app.core.settings import settings


@pytest.mark.unit
@pytest.mark.security
class TestJWTAuthentication:
    def test_create_access_token(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_with_expiry(self):
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta=expires_delta)
        
        assert token is not None
        decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        assert "exp" in decoded
        assert decoded["sub"] == "testuser"
    
    def test_decode_valid_token(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        decoded = decode_token(token)
        
        assert decoded is not None
        assert decoded.get("sub") == "testuser"
    
    def test_decode_expired_token(self):
        data = {"sub": "testuser"}
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta=expires_delta)
        
        decoded = decode_token(token)
        
        assert decoded is None
    
    def test_decode_invalid_token(self):
        invalid_token = "invalid.token.here"
        
        decoded = decode_token(invalid_token)
        
        assert decoded is None
    
    def test_decode_tampered_token(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        tampered_token = token[:-10] + "tampered12"
        
        decoded = decode_token(tampered_token)
        
        assert decoded is None
    
    def test_token_contains_required_claims(self):
        data = {"sub": "testuser", "role": "admin"}
        token = create_access_token(data)
        
        decoded = decode_token(token)
        
        assert decoded is not None
        assert "sub" in decoded
        assert "exp" in decoded
        assert decoded.get("role") == "admin"
