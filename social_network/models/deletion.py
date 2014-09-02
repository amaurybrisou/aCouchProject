# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from commons.base import Base



# Create your models here.
class Deletion(Base):
    __table_args__ = { 'schema': 'social_network'}

    id = Column(Integer, primary_key=True)
    request_date = Column(DateTime)
    effective_date = Column(DateTime)

    # account_id_fk = Column(Integer,  ForeignKey('account.id'))
    
    deletion_reason_id_fk = Column(Integer, 
        ForeignKey('social_network.deletion_reason.id'))


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Deletion, self).save(force_insert, force_update)