"""AWS Active Directory Authentication Service"""
from typing import Optional, Dict
from ldap3 import Server, Connection, ALL, NTLM
import os
from datetime import timedelta
from app.utils.auth_helpers import create_access_token


class AWSADAuthService:
    """Service for authenticating users against AWS Active Directory"""
    
    def __init__(self):
        self.ad_server = os.getenv("AWS_AD_SERVER")
        self.ad_domain = os.getenv("AWS_AD_DOMAIN")
        self.ad_base_dn = os.getenv("AWS_AD_BASE_DN")
        self.ad_use_ssl = os.getenv("AWS_AD_USE_SSL", "true").lower() == "true"
        
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        Authenticate user against AWS Active Directory
        
        Args:
            username: User's username (without domain)
            password: User's password
            
        Returns:
            User information dict if authenticated, None otherwise
        """
        if not self.ad_server or not self.ad_domain:
            raise ValueError("AWS AD configuration is missing. Please set AWS_AD_SERVER and AWS_AD_DOMAIN environment variables.")
        
        try:
            # Create LDAP server connection
            server = Server(
                self.ad_server,
                use_ssl=self.ad_use_ssl,
                get_info=ALL
            )
            
            # Format username with domain for NTLM authentication
            user_dn = f"{self.ad_domain}\\{username}"
            
            # Attempt to bind with user credentials
            conn = Connection(
                server,
                user=user_dn,
                password=password,
                authentication=NTLM,
                auto_bind=True
            )
            
            if conn.bind():
                # Get user information
                user_info = self._get_user_info(conn, username)
                conn.unbind()
                return user_info
            else:
                return None
                
        except Exception as e:
            print(f"LDAP Authentication Error: {str(e)}")
            return None
    
    def _get_user_info(self, conn: Connection, username: str) -> Dict:
        """
        Retrieve user information from Active Directory
        
        Args:
            conn: Active LDAP connection
            username: Username to search for
            
        Returns:
            Dictionary containing user information
        """
        try:
            # Search for user in AD
            search_filter = f"(sAMAccountName={username})"
            conn.search(
                search_base=self.ad_base_dn or "",
                search_filter=search_filter,
                attributes=['mail', 'displayName', 'memberOf', 'department']
            )
            
            if conn.entries:
                entry = conn.entries[0]
                return {
                    "username": username,
                    "email": str(entry.mail) if hasattr(entry, 'mail') else f"{username}@{self.ad_domain}",
                    "display_name": str(entry.displayName) if hasattr(entry, 'displayName') else username,
                    "department": str(entry.department) if hasattr(entry, 'department') else None,
                    "groups": [str(g) for g in entry.memberOf] if hasattr(entry, 'memberOf') else []
                }
            else:
                # Fallback if user info not found
                return {
                    "username": username,
                    "email": f"{username}@{self.ad_domain}",
                    "display_name": username,
                    "department": None,
                    "groups": []
                }
        except Exception as e:
            print(f"Error fetching user info: {str(e)}")
            # Return basic info if fetch fails
            return {
                "username": username,
                "email": f"{username}@{self.ad_domain}",
                "display_name": username,
                "department": None,
                "groups": []
            }
    
    def create_user_token(self, user_info: Dict) -> str:
        """
        Create JWT token for authenticated user
        
        Args:
            user_info: User information dictionary
            
        Returns:
            JWT token string
        """
        token_data = {
            "sub": user_info["username"],
            "email": user_info["email"],
            "name": user_info["display_name"],
            "department": user_info.get("department")
        }
        
        # Create token with 8 hour expiration
        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(hours=8)
        )
        
        return access_token


# Singleton instance
_ad_auth_service = None

def get_ad_auth_service() -> AWSADAuthService:
    """Get singleton instance of AWS AD Auth Service"""
    global _ad_auth_service
    if _ad_auth_service is None:
        _ad_auth_service = AWSADAuthService()
    return _ad_auth_service
