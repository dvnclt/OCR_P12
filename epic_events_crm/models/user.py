from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column('password', String)
    role = Column(String)  # 'gestion', 'commercial', 'support'

    clients = relationship('Client', back_populates='user')
    contracts = relationship('Contract', back_populates='user')
    events = relationship('Event', back_populates='user')
