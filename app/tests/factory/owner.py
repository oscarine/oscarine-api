from sqlalchemy.orm import Session

from app.api.utils.otp import generate_random_otp
from app.core.jwt import create_access_token
from app.core.security import get_password_hash
from app.db_models.owner import Owner
from app.tests.factory.base import Base


class OwnerFactory(Base):
    def __init__(self) -> None:
        self.id = None
        self.email = self.random_email()
        self.password = self.random_lower_string()
        self.otp = generate_random_otp()

    def create(self, db: Session):
        owner = Owner(
            email=self.email,
            password_hash=get_password_hash(self.password),
            otp=self.otp,
        )
        db.add(owner)
        db.commit()
        db.refresh(owner)
        self.id = owner.id

    def get_auth_token(self) -> str:
        return create_access_token(data={"owner_id": self.id})
