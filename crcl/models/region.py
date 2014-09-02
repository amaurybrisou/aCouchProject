# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from commons.base import Base


# Create your models here.
class Region(Base):
    __table_args__ = { 'schema': 'crcl'}

    id = Column(Integer, primary_key=True)
    country_id_fk = Column(Integer, ForeignKey('crcl.country.id'))
    name = Column(String(45), nullable=False)
    code = Column(String(8), nullable=False)
    adm1ode = Column(String(4), nullable=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Region, self).save(force_insert, force_update)