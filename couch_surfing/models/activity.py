# -*- coding: utf-8 -*-

from sqlalchemy import Column, Table, Integer, Boolean,String, ForeignKey, ForeignKeyConstraint, DateTime
from sqlalchemy.orm import relationship, backref
from util.dates import Dates
from couch_surfing.models.couch import Couch
from couch_surfing.models.geo_loc import Geoloc

from commons.base import Base


# Create your models here.
class Activity(Base):


    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    difficulty = Column(String(50), nullable=False)


    association_table_geo_loc = Table('rel_activity_geo_loc', Base.metadata,
        Column('activity_id_fk', Integer, ForeignKey('activity.id'),
            primary_key=True),
        Column('geo_loc_id_fk', Integer, ForeignKey('geo_loc.id'),
            primary_key=True)
    )
    pages = relationship("Geoloc",
        secondary=association_table_geo_loc,
        backref="activities")
    


    association_table_couch = Table('rel_activity_couch', Base.metadata,
        Column('activity_id_fk', Integer, ForeignKey('activity.id'),
            primary_key=True),
        Column('couch_id_fk', Integer, ForeignKey('couch.id'),
            primary_key=True)
    )
    pages = relationship("Couch",
        secondary=association_table_couch,
        backref="activities")

    