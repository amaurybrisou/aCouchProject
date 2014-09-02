# -*- coding: utf-8 -*-

from sqlalchemy import Column, Table, CHAR, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import datetime, uuid
from commons.base import Base

# Create your models here.
class Email(Base):
    __table_args__ = { 'schema': 'social_network'}

    id = Column(Integer, primary_key=True)
    address = Column(String(50), nullable=False, unique=True)
    insert_date = Column(DateTime, nullable=False,
        default=datetime.datetime.utcnow)
    validation_date = Column(DateTime, nullable=True)
    mail_type = Column(String(12), nullable=False, default="main")
    token = Column(CHAR(32), nullable=False, unique=True)
    registered = Column(Integer, default=0 )


    def __init__(self, address, mail_type="main", registered=0):
        self.address = address
        self.mail_type = mail_type
        self.token = uuid.uuid4().hex
        self.registered = registered

   
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Email, self).save(force_insert, force_update)