from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password, verify_password, create_access_token
from app.schemas.auth import TokenResponse


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).one_or_none()


def create_user(db: Session, name: str, email: str, password: str) -> User:
    hashed = hash_password(password)
    user = User(name=name, email=email, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_token_for_user(user: User) -> TokenResponse:
    payload = {"user_id": user.id}
    access_token = create_access_token(payload)
    return TokenResponse(access_token=access_token)
