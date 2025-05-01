import pytest
from typing import Optional
from app.core.interfaces.users_repository_interface import (
    UsersRepositoryInterface,
    PasswordHasherInterface
)
from app.models.user import User
from app.services.authentication_service import AuthenticationService
from unittest.mock import patch
from app.models.user_role import UserRole


class MockUserRepository(UsersRepositoryInterface):
    def getUserByUsername(self, username: str) -> Optional[User]:
        if username == "existing_user":
            return User(username="existing_user", firstName="First",
                        lastName="Last", passwordHash="hashed_password",
                        role=UserRole.ADMIN)
        return None

    def insertUser(self, user: User) -> None:
        pass


class MockPasswordHasher(PasswordHasherInterface):
    def hash(self, password: str) -> str:
        return "hashed_password"

    def verify(self, password: str, hash: str) -> bool:
        return password == "password" and hash == "hashed_password"


@pytest.fixture
def mock_user_repository():
    return MockUserRepository()


@pytest.fixture
def mock_password_hasher():
    return MockPasswordHasher()


def test_authenticate_user_existing_user(mock_user_repository,
                                         mock_password_hasher):

    auth_service = AuthenticationService(mock_user_repository,
                                         mock_password_hasher)
    result = auth_service.authenticateUser("existing_user", "password")
    assert result is True


def test_authenticate_user_non_existing_user(mock_user_repository,
                                             mock_password_hasher):

    auth_service = AuthenticationService(mock_user_repository,
                                         mock_password_hasher)
    result = auth_service.authenticateUser("non_existing_user", "password")
    assert result is False


def test_generate_username(mock_user_repository, mock_password_hasher):
    service = AuthenticationService(mock_user_repository, mock_password_hasher)

    with patch("app.services.authentication_service.random.randint",
               return_value=123):
        username = service.generateUsername("John", "Doe")

    assert username == "john.doe.123"
