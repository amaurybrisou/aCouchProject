# -*- coding: utf-8 -*-

from sqlalchemy import Column, Table, Float, Integer, Boolean,String, ForeignKey, ForeignKeyConstraint, DateTime
from sqlalchemy.orm import relationship, backref

from commons.base import Base


class Matrice(Base):
	id = Column(Integer, primary_key=True)
	size = Column(Integer, nullable=False)
	alone = Column(Boolean, nullable=False)
	sheet = Column(Boolean, nullable=False)