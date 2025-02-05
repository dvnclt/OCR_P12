from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates

from config.config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column('password', String)
    role_name = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))

    clients = relationship('Client', back_populates='user')
    contracts = relationship('Contract', back_populates='user')
    events = relationship('Event', back_populates='user')
    role = relationship("Role", back_populates="users")

    @validates('role_id')
    def update_role_name(self, key, role_id):
        """Met à jour le nom du rôle lors de la modification du role_id."""
        if role_id:
            role = self.role
            self.role_name = role.name if role else None
        return role_id


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    permissions = Column(String)

    users = relationship("User", back_populates="role")
