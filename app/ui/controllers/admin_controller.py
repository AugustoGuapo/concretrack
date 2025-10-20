from app.services.authentication_service import AuthenticationService
from app.services.implementations.user_repository_impl import UserRepositoryImpl
from app.services.implementations.bcrypt_hasher_impl import BcryptHasherImpl
from app.services.implementations.fingerprint_impl import FingerprintImpl
from app.core.exceptions.fingerprint_exceptions import SensorStorageException
from app.models.user_role import UserRole  # 🔹 Import necesario


class AdminController:
    def __init__(self):
        self.auth_service = AuthenticationService(UserRepositoryImpl(), BcryptHasherImpl())
        self.user_repo = UserRepositoryImpl()  # acceso directo al repositorio

    # Crear usuario (con o sin huella)
    def create_user(self, firstName, lastName, password, role, fingerprintId=None):
        # 🔹 Verificar que el rol sea válido
        if not role:
            raise ValueError("El rol no puede ser None. Selecciona un rol válido.")

        # 🔹 Convertir el rol a UserRole si viene como string
        if isinstance(role, str):
            try:
                role = UserRole[role.upper()]
            except KeyError:
                raise ValueError(f"Rol inválido: {role}")

        # Registrar usuario con is_active=1
        return self.auth_service.registerUser(
            firstName=firstName,
            lastName=lastName,
            password=password,
            role=role,
            fingerprintId=fingerprintId
        )

    # Obtener todos los usuarios activos
    def get_all_users(self):
        return self.user_repo.getAllActiveUsers()

    # Editar usuario existente
    def update_user(self, user_id, first_name, last_name, role, password=None):
        """Actualiza los datos del usuario (nombre, apellido, rol y contraseña opcional)."""
        # Si el usuario ingresó una nueva contraseña
        if password and password.strip():
            hasher = BcryptHasherImpl()
            password_hash = hasher.hash(password)
            self.user_repo.updateUser(user_id, first_name, last_name, role, password_hash)
        else:
            # Si no cambia la contraseña, mantenla igual
            self.user_repo.updateUser(user_id, first_name, last_name, role)


    # Eliminar usuario lógicamente (is_active = 0)
    def delete_user_logically(self, user_id):
        self.user_repo.logicalDeleteUser(user_id)
