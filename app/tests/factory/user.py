from sqlalchemy.orm import Session

from app.api.utils.otp import generate_random_otp
from app.core.jwt import create_access_token
from app.core.security import get_password_hash
from app.db_models.user import User
from app.tests.factory.base import Base


class UserFactory(Base):
    def __init__(self) -> None:
        self.email = self.random_email()
        self.password = self.random_lower_string()
        self.otp = generate_random_otp()

    def create(self, db: Session) -> None:
        user = User(
            email=self.email, password_hash=get_password_hash(self.password), otp=self.otp
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        self.id = user.id

    def get_auth_token(self) -> str:
        return create_access_token(data={"user_id": self.id})

    @staticmethod
    def get_by_id(db: Session, id: int) -> User:
        return db.query(User).filter_by(id=id).first()
