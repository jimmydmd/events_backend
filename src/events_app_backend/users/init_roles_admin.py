# poetry run python src/events_app_backend/users/init_roles_admin.py
import uuid
from sqlmodel import Session, select
from events_app_backend.core.database import engine
from events_app_backend.users.models import User
from events_app_backend.roles.models import Role
from events_app_backend.core.security import hash_password

def init_roles_and_admin():
    with Session(engine) as session:
        # --- Roles ---
        roles_data = [
            {"name": "Admin", "description": "Control total del sistema"},
            {"name": "Organizer", "description": "Gestiona sus propios eventos"},
            {"name": "Participant", "description": "Usuario normal que puede inscribirse"},
        ]

        role_objs = {}
        for r in roles_data:
            role = session.exec(select(Role).where(Role.name == r["name"])).first()
            if not role:
                role = Role(name=r["name"], description=r["description"])
                session.add(role)
                session.commit()
                session.refresh(role)
                print(f"Role '{r['name']}' created.")
            role_objs[r["name"]] = role

        # --- Usuario Admin ---
        admin_email = "admin@example.com"
        existing_admin = session.exec(select(User).where(User.email == admin_email)).first()
        if existing_admin:
            print("Admin user already exists")
            return

        admin_user = User(
            first_name="Admin",
            last_name="User",
            email=admin_email,
            password=hash_password("admin123"),  # Cambia la contraseña por seguridad
            role_id=role_objs["Admin"].id
        )
        session.add(admin_user)
        session.commit()
        session.refresh(admin_user)
        print(f"Admin user '{admin_email}' created with role Admin.")

if __name__ == "__main__":
    init_roles_and_admin()
