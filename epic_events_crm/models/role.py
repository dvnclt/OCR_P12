from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from config.config import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    permissions = relationship('Permission', secondary='role_permissions',
                               back_populates='roles')
    users = relationship('User', back_populates='role')


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    roles = relationship('Role', secondary='role_permissions',
                         back_populates='permissions')


role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'),
           primary_key=True)
)
