from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from config.config import Base


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    location = Column(String)
    attendees = Column(Integer)
    contact = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    notes = Column(String)

    client = relationship('Client', back_populates='events')
    contract = relationship('Contract', back_populates='events')
    user = relationship('User', back_populates='events')
