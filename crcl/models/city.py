# -*- coding: utf-8 -*-

from sqlalchemy import Column, Float, Integer, String, ForeignKey, DateTime
from commons.base import Base


# Create your models here.
class City(Base):
    __table_args__ = { 'schema': 'crcl'}
    
    id = Column(Integer, primary_key=True)
    country_id_fk = Column(Integer, ForeignKey('crcl.country.id'))
    region_id_fk = Column(Integer, ForeignKey('crcl.region.id'))
    name = Column(String(45), nullable=False)
    latitude = Column(Float(asdecimal=True, decimal_return_scale=2), nullable=False)
    longitude = Column(Float(asdecimal=True, decimal_return_scale=2), nullable=False)
    timezone = Column(String(10), nullable=False)
    dma_id = Column(Integer)
    code = Column(String(4))


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(City, self).save(force_insert, force_update)