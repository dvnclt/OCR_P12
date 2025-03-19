import uuid

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import date

from config.config import Base


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True,
                default=uuid.uuid4)
    client_id = Column(Integer, ForeignKey('clients.id'))
    total_amount = Column(Numeric(10, 2))
    paid_amount = Column(Numeric(10, 2))
    remaining_amount = Column(Numeric(10, 2))
    creation_date = Column(Date, default=date.today())
    status = Column(String)
    contact = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    client = relationship('Client', back_populates='contracts')
    user = relationship('User', back_populates='contracts')
    events = relationship('Event', back_populates='contract')
