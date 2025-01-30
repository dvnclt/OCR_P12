from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from config.config import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    client = relationship('Client', back_populates='users')
    contract = relationship('Contract', back_populates='users')
    event = relationship('Event', back_populates='users')
    role = relationship("Role", back_populates="users")

    def set_password(self, password: str):
        # Hash le mot de passe avant de le stocker
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str):
        # Vérifie si le mot de passe correspond au hash stocké
        return pwd_context.verify(password, self.hashed_password)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="role")
