"""
Ejemplos de peticiones API para probar los endpoints de autenticación
Puedes usar estos ejemplos con herramientas como Postman, Insomnia, o curl
"""

# ============================================
# 1. REGISTRO DE USUARIO
# ============================================
"""
POST http://localhost:8000/api/auth/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User",
    "phone": "+1234567890"
}

Respuesta esperada (201 Created):
{
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890",
        "created_at": "2024-01-14T12:00:00Z"
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "message": "User registered successfully"
}
"""

# ============================================
# 2. INICIO DE SESIÓN
# ============================================
"""
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "SecurePass123!"
}

Respuesta esperada (200 OK):
{
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890",
        "created_at": "2024-01-14T12:00:00Z"
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "message": "Login successful"
}
"""

# ============================================
# 3. VER PERFIL (requiere autenticación)
# ============================================
"""
GET http://localhost:8000/api/auth/profile/
Authorization: Bearer {access_token}

Respuesta esperada (200 OK):
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "phone": "+1234567890",
    "created_at": "2024-01-14T12:00:00Z"
}
"""

# ============================================
# 4. ACTUALIZAR PERFIL (requiere autenticación)
# ============================================
"""
PUT http://localhost:8000/api/auth/profile/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "first_name": "Updated",
    "last_name": "Name",
    "phone": "+9876543210"
}

Respuesta esperada (200 OK):
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Updated",
    "last_name": "Name",
    "phone": "+9876543210",
    "created_at": "2024-01-14T12:00:00Z"
}
"""

# ============================================
# 5. CAMBIAR CONTRASEÑA (requiere autenticación)
# ============================================
"""
POST http://localhost:8000/api/auth/change-password/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "old_password": "SecurePass123!",
    "new_password": "NewSecurePass456!",
    "new_password2": "NewSecurePass456!"
}

Respuesta esperada (200 OK):
{
    "message": "Password changed successfully"
}
"""

# ============================================
# 6. REFRESCAR TOKEN
# ============================================
"""
POST http://localhost:8000/api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "{refresh_token}"
}

Respuesta esperada (200 OK):
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
"""

# ============================================
# 7. CERRAR SESIÓN (requiere autenticación)
# ============================================
"""
POST http://localhost:8000/api/auth/logout/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "refresh": "{refresh_token}"
}

Respuesta esperada (200 OK):
{
    "message": "Logout successful"
}
"""

# ============================================
# EJEMPLOS CON CURL
# ============================================

# Registro
"""
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
"""

# Login
"""
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!"
  }'
"""

# Ver perfil (reemplaza YOUR_ACCESS_TOKEN con tu token)
"""
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
"""

# ============================================
# EJEMPLOS CON PYTHON REQUESTS
# ============================================
"""
import requests

BASE_URL = "http://localhost:8000/api/auth"

# Registro
response = requests.post(
    f"{BASE_URL}/register/",
    json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!",
        "password2": "SecurePass123!",
        "first_name": "Test",
        "last_name": "User"
    }
)
print(response.json())

# Login
response = requests.post(
    f"{BASE_URL}/login/",
    json={
        "username": "testuser",
        "password": "SecurePass123!"
    }
)
data = response.json()
access_token = data['access']
print(f"Access Token: {access_token}")

# Ver perfil
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(f"{BASE_URL}/profile/", headers=headers)
print(response.json())
"""
