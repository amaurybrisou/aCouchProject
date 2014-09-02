# -*- coding: utf-8 -*-

#from json import dumps
import simplejson as json
from decimal import Decimal
from sqlalchemy.ext.declarative import declarative_base, declared_attr

class Base(object):
    class Meta:
        app_label = 'aCouch'

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}

    def toJSON(self):
        r = {}
    	for c in self._sa_class_manager.mapper.mapped_table.columns:
            v = getattr(self, c.name)
            if isinstance(v, Decimal):
                v = round(v,2)
            r[c.name] = v
        return r

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(self.__class__, self).save(force_insert, force_update)

Base = declarative_base(cls=Base)