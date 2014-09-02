# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Enum, Float, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from crcl.models.language import Language
from crcl.models.region import Region

from commons.base import Base


# Create your models here.
class Country(Base):
    __table_args__ = { 'schema': 'crcl'}
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    fips104 = Column(String(2), nullable=False)
    iso2 = Column(String(2), nullable=False)
    iso3 = Column(String(3), nullable=False)
    ison = Column(String(4), nullable=False)
    internet = Column(String(2), nullable=False)
    capital = Column(String(25))
    mapreference = Column(String(50))
    nationality_singular = Column(String(35))
    nationality_plural = Column(String(35))
    currency = Column(String(30))
    currency_code = Column(String(3))
    population = Column(Integer)
    title = Column(String(50))
    comment = Column(String(255))

    regions = relationship('Region', order_by='Region.id',
        backref='country')

    association_table = Table('rel_country_language', Base.metadata,
        Column('country_id_fk', Integer, ForeignKey('crcl.country.id'), 
            primary_key=True),
        Column('language_id_fk', Integer, ForeignKey('crcl.language.id'),
            primary_key=True),
        schema='crcl',
        # Column('is_official', Enum('T', 'F', name='boolean'), nullable=False, default='F'),
        #Column('percentage', Float(4,1), nullable=False, default=0.0)
    )
    languages = relationship('Language', order_by='Language.name',
        backref='countries', secondary=association_table)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Country, self).save(force_insert, force_update)