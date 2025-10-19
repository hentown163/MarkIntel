# JWT Authentication with AWS Active Directory Integration

This application now includes a complete JWT-based authentication system with AWS Active Directory (AD) integration.

## 🔐 Features

- **JWT Token Authentication**: Secure token-based authentication with 8-hour expiration
- **AWS Active Directory Integration**: Authenticate users against your AWS AD/LDAP server
- **Protected API Routes**: All API endpoints require authentication
- **Login Page**: Clean, modern login interface
- **Automatic Token Management**: Frontend automatically includes auth tokens in all API requests
- **Session Persistence**: Users stay logged in across page refreshes
- **Logout Functionality**: Secure logout with token cleanup

## ⚙️ Configuration

### 1. JWT Secret Key (Already Configured)

The JWT secret key has been set up in your Replit Secrets. This key is used to sign and verify authentication tokens.

### 2. AWS Active Directory Settings

To enable AWS AD authentication, you need to add these secrets to your Replit Secrets:

1. Click on the "Secrets" tab (🔒) in the left sidebar
2. Add the following secrets:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `AWS_AD_SERVER` | Your AWS AD server hostname | `ad.example.com` or `10.0.1.100` |
| `AWS_AD_DOMAIN` | Your AD domain name | `MYCOMPANY` or `EXAMPLE` |
| `AWS_AD_BASE_DN` | Base Distinguished Name for user searches | `DC=example,DC=com` |
| `AWS_AD_USE_SSL` | Use SSL/TLS for LDAP connection | `true` or `false` |

#### Example Configuration:

```
AWS_AD_SERVER=ad.mycompany.com
AWS_AD_DOMAIN=MYCOMPANY
AWS_AD_BASE_DN=DC=mycompany,DC=com
AWS_AD_USE_SSL=true
```

## 🧪 Testing the Authentication

### Without AWS AD (Development/Testing)

If you haven't configured AWS AD yet, you'll see a helpful error message when trying to log in explaining what needs to be configured.

### With AWS AD Configured

1. **Access the login page**: Navigate to `/login` or just visit the root URL (you'll be redirected)
2. **Enter credentials**: Use your AWS AD username and password
3. **Successful login**: You'll be redirected to the dashboard
4. **Access protected routes**: All API calls now include your authentication token

### Testing the API Directly

You can test the authentication endpoints using curl or any API client:

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"your-username","password":"your-password"}'
```

**Get current user info:**
```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Check auth health:**
```bash
curl http://localhost:8000/api/auth/health
```

## 🔒 Security Features

1. **Secure Token Generation**: Uses industry-standard JWT with strong secret key
2. **Token Expiration**: Tokens expire after 8 hours for security
3. **HTTPS Support**: LDAP connections support SSL/TLS
4. **Password Security**: Passwords are never logged or stored
5. **Protected Routes**: All API endpoints require valid authentication

## 📝 API Endpoints

### Authentication Endpoints (Public)

- `POST /api/auth/login` - Login with username/password
- `GET /api/auth/health` - Check authentication service status

### Authentication Endpoints (Protected)

- `GET /api/auth/me` - Get current user information
- `POST /api/auth/logout` - Logout (client discards token)

### Protected Application Endpoints

All the following endpoints now require authentication:

- `/api/campaigns/*` - Campaign management
- `/api/services/*` - Service information
- `/api/market-intelligence/*` - Market intelligence data
- `/api/dashboard/*` - Dashboard metrics

## 🎨 Frontend Components

### Login Page
- Located at: `frontend/src/pages/LoginPage.jsx`
- Clean, modern design with error handling
- Form validation and loading states

### Authentication Context
- Located at: `frontend/src/context/AuthContext.jsx`
- Manages authentication state across the app
- Provides login/logout functions

### Protected Routes
- Located at: `frontend/src/components/ProtectedRoute.jsx`
- Automatically redirects unauthenticated users to login
- Handles loading states gracefully

### Navbar Updates
- Shows current user information
- Logout button
- Responsive design

## 🛠️ Troubleshooting

### "JWT_SECRET_KEY must be set" Error
- The JWT secret is already configured in your Replit Secrets
- If you see this error, the secret may not have been picked up. Restart the backend workflow.

### "AWS AD configuration is missing" Error
- You need to add the AWS AD secrets (see Configuration section above)
- This is expected if you haven't configured AD yet

### "Invalid username or password" Error
- Check that your AWS AD credentials are correct
- Verify the AWS AD server is accessible from Replit
- Check the backend logs for more details about the LDAP connection

### Users Immediately Redirected to Login
- Check browser console for errors
- Verify the token is being stored in localStorage
- Check that the API is returning valid tokens

### 401 Unauthorized on API Calls
- Token may have expired (8 hour limit)
- Token may be invalid
- Try logging out and logging back in

## 📚 Code Structure

### Backend (Python/FastAPI)

```
app/
├── api/
│   └── auth.py                    # Authentication endpoints
├── core/
│   ├── auth_middleware.py         # JWT validation middleware
│   └── settings.py                # Configuration with AD settings
├── services/
│   └── aws_ad_auth.py            # AWS AD authentication service
└── utils/
    └── auth_helpers.py            # JWT token utilities
```

### Frontend (React)

```
frontend/src/
├── pages/
│   └── LoginPage.jsx              # Login page component
├── context/
│   └── AuthContext.jsx            # Authentication state management
├── components/
│   ├── ProtectedRoute.jsx         # Route protection wrapper
│   └── Navbar.jsx                 # Updated with user info & logout
└── api/
    └── client.js                  # API client with auth interceptors
```

## 🚀 Next Steps

1. **Configure AWS AD**: Add the AWS AD secrets to enable real authentication
2. **Test Login**: Try logging in with your AD credentials
3. **Customize Token Expiration**: Modify `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` in settings if needed
4. **Add User Roles**: Extend the system to support role-based access control
5. **Audit Logging**: Track login attempts and access patterns

## 📖 Additional Resources

- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io - Introduction to JSON Web Tokens](https://jwt.io/introduction/)
- [LDAP3 Python Library Documentation](https://ldap3.readthedocs.io/)
