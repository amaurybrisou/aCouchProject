# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from commons.base import Base

# Create your models here.
class Deletion_Reason(Base):
    __table_args__ = { 'schema': 'social_network'}

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Deletion_Reason, self).save(force_insert, force_update)