# -*- coding: utf-8 -*-

from sqlalchemy import Column, Table, Float, Integer, Boolean,String, ForeignKey, ForeignKeyConstraint, DateTime
from sqlalchemy.orm import relationship, backref

from commons.base import Base


class Option(Base):
	id = Column(Integer, primary_key=True)
	name = Column(String(64), nullable=False)
	details = Column(String(64), nullable=False)
