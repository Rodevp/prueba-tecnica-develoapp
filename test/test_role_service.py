import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from sqlalchemy import exc 
from app.roles.services import assign_permission_to_role

class MockRole:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MockPermission:
    def __init__(self, id, name):
        self.id = id
        self.name = name


@patch('app.role_models.RolePermission')
@patch('app.role_models.Role')
@patch('app.role_models.Permission')
def test_assign_permissions_to_role_success(MockPermission, MockRole, MockRolePermission):
    """Verifica la asignación exitosa de múltiples permisos a un rol."""
    mock_db = MagicMock()
    role_id = 3
    permission_names = ["fields:create", "dashboard:view", "roles:view"]

    MockRole.query.return_value.filter.return_value.first.return_value = MockRole(id=role_id, name="sub_gerente")

    mock_permissions = [
        MockPermission(id=10, name="fields:create"),
        MockPermission(id=11, name="dashboard:view"),
        MockPermission(id=12, name="roles:view")
    ]
    MockPermission.query.return_value.filter.return_value.all.return_value = mock_permissions

    result = assign_permission_to_role(mock_db, role_id, permission_names)
    
    assert MockRolePermission.call_count == 3
    
    mock_db.bulk_save_objects.assert_called_once()
    
    mock_db.commit.assert_called_once()
    
    assert "Se agregaron 3 permisos" in result['message']

@patch('app.role_models.Role')
def test_assign_permissions_to_role_role_not_found(MockRole):
    """Verifica HTTPException si el rol no existe."""
    mock_db = MagicMock()
    role_id = 999
    
    MockRole.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        assign_permission_to_role(mock_db, role_id, ["some:perm"])
    
    assert excinfo.value.status_code == 404
    assert "Rol con ID 999 no encontrado" in excinfo.value.detail
    mock_db.commit.assert_not_called()
    

@patch('app.role_models.RolePermission')
@patch('app.role_models.Role')
@patch('app.role_models.Permission')
def test_assign_permissions_to_role_duplicate_error(MockPermission, MockRole, MockRolePermission):
    """Verifica el rollback en caso de error de integridad (permiso duplicado)."""
    mock_db = MagicMock()
    role_id = 4
    permission_names = ["fields:create"]

    MockRole.query.return_value.filter.return_value.first.return_value = MockRole(id=role_id, name="test_role")
    MockPermission.query.return_value.filter.return_value.all.return_value = [MockPermission(id=10, name="fields:create")]

    mock_db.bulk_save_objects.side_effect = exc.IntegrityError(statement=None, params=None, orig=None)

    with pytest.raises(HTTPException) as excinfo:
        assign_permission_to_role(mock_db, role_id, permission_names)

    assert excinfo.value.status_code == 400
    assert "Error de integridad" in excinfo.value.detail
    
    mock_db.commit.assert_called_once() 
    mock_db.rollback.assert_called_once()