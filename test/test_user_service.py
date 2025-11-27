import pytest
from unittest.mock import MagicMock, patch 
from fastapi import HTTPException
from app.auth.services import register_user 

class MockUserData:
    email = "test_nuevo@example.com"
    full_name = "Test User"
    password = "secure_password"
    role_name = "user"

def mock_get_role_id_by_name():
    return 2 

def mock_hash_password(password: str):
    return f"hashed_{password}"

@patch('app.auth.services.hash_password', side_effect=mock_hash_password)
@patch('app.auth.services.get_role_id_by_name', side_effect=mock_get_role_id_by_name)
@patch('app.auth.models.User') 
def test_register_user_success(MockUserModel, mock_hash_password):
    """Verifica que el usuario se registre correctamente y que se interactúe con la DB."""
    mock_db = MagicMock()
    user_data = MockUserData()
    
    mock_db.query.return_value.filter.return_value.first.return_value = None

    register_user(mock_db, user_data)
    mock_hash_password.assert_called_once_with("secure_password")
    
    MockUserModel.assert_called_once_with(
        email=user_data.email,
        full_name=user_data.full_name,
        password='hashed_secure_password', 
        role_id=2 
    )
    
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_register_user_already_exists():
    """Verifica que se lance HTTPException si el email ya existe."""
    mock_db = MagicMock()
    user_data = MockUserData()
    
    mock_db.query.return_value.filter.return_value.first.return_value = 'existing_user_object'
    with pytest.raises(HTTPException) as excinfo:
        register_user(mock_db, user_data)
    
    assert excinfo.value.status_code == 400
    assert "El correo ya está registrado" in excinfo.value.detail
    
    mock_db.commit.assert_not_called()