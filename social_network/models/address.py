# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint

from crcl.models.city import City

from commons.base import Base


# Create your models here.
class Address(Base):

    id = Column(Integer, primary_key=True)
    street_number = Column(Integer, nullable=False)
    street_name = Column(String(64), nullable=False)
    city_id_fk = Column(Integer, ForeignKey('crcl.city.id'), 
        nullable=False),
    UniqueConstraint(
            'street_name',
            'street_number',
            'city_id_fk',
            name='unique_address'),

    __table_args__ = { 'schema': 'social_network'}



    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Address, self).save(force_insert, force_update)