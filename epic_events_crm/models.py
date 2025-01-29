from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date

from config.config import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    company_name = Column(String)
    creation_date = Column(Date, default=date.today())
    last_update_date = Column(Date, default=date.today())
    sales_contact_id = Column(Integer, ForeignKey('collaborators.id'))

    contracts = relationship('Contract', back_populates='client')
    events = relationship('Event', back_populates='client')
    sales_contact = relationship('Collaborator', back_populates='clients')


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    contract_amount = Column(Integer)
    remaining_amount = Column(Integer)
    creation_date = Column(Date, default=date.today())
    contract_status = Column(String)
    sales_contact_id = Column(Integer, ForeignKey('collaborators.id'))

    client = relationship('Client', back_populates='contracts')
    sales_contact = relationship('Collaborator', back_populates='contracts')
    event = relationship('Event', back_populates='contract')


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
    support_contact_id = Column(Integer, ForeignKey('collaborators.id'))
    notes = Column(String)

    client = relationship('Client', back_populates='events')
    contract = relationship('Contract', back_populates='event')
    support_contact = relationship('Collaborator', back_populates='events')


class Collaborator(Base):
    __tablename__ = 'collaborators'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True)
    role = Column(String, index=True)

    clients = relationship('Client', back_populates='sales_contact')
    contracts = relationship('Contract', back_populates='sales_contact')
    events = relationship('Event', back_populates='support_contact')
