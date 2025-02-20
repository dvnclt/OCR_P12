from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date

from config.config import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    company_name = Column(String)
    creation_date = Column(Date, default=date.today())
    last_update_date = Column(Date, default=date.today())
    contact = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    contracts = relationship('Contract', back_populates='client')
    events = relationship('Event', back_populates='client')
    user = relationship('User', back_populates='clients')
