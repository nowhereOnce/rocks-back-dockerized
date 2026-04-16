import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_signup_user(client):
    """Prueba que un usuario pueda registrarse exitosamente."""
    response = await client.post(
        "/auth/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_login_user(client):
    """Prueba que un usuario pueda iniciar sesión y obtener un token."""
    # Primero registramos al usuario
    await client.post(
        "/auth/signup",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "loginpassword",
            "first_name": "Login",
            "last_name": "User"
        }
    )

    # Intentamos login
    response = await client.post(
        "/auth/token",
        data={
            "username": "loginuser",
            "password": "loginpassword"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_user(client):
    """Prueba que el login falle con credenciales incorrectas."""
    response = await client.post(
        "/auth/token",
        data={
            "username": "nonexistent",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect username or password"
