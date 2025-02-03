from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date

from config.config import Base


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    contract_amount = Column(Integer)
    remaining_amount = Column(Integer)
    creation_date = Column(Date, default=date.today())
    contract_status = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    client = relationship('Client', back_populates='contracts')
    user = relationship('User', back_populates='contracts')
    events = relationship('Event', back_populates='contract')
