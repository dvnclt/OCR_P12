from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from epic_events_crm.config.config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    client = relationship('Client', back_populates='users')
    contract = relationship('Contract', back_populates='users')
    event = relationship('Event', back_populates='users')
    role = relationship("Role", back_populates="users")


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="role")
