# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from commons.base import Base


# Create your models here.
class Language(Base):
    __table_args__ = { 'schema': 'crcl'}

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    native_name = Column(String(255), unique=False)
    speakers = Column(Float(precision=2, asdecimal=True, decimal_return_scale=2))
    percentage = Column(Float(precision=2, asdecimal=True, decimal_return_scale=2))

    def insert(self, id, name):
    	super(Language, self, id, name).save(force_insert, force_update)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Language, self).save(force_insert, force_update)