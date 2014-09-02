# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref

from commons.base import Base

# Create your models here.
class Status(Base):
    __table_args__ = { 'schema': 'social_network'}

    name = Column(String(255), primary_key=True)
   
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Status, self).save(force_insert, force_update)