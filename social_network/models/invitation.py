# -*- coding: utf-8 -*-

from sqlalchemy import Column, Table, Integer, String, UniqueConstraint, ForeignKey, ForeignKeyConstraint, DateTime
from sqlalchemy.orm import relationship, backref
from commons.util.dates import Dates
from social_network.models.status import Status

from commons.base import Base


# Create your models here.
class Invitation(Base):
    __table_args__ = { 'schema': 'social_network'}

    id = Column(Integer, primary_key=True)
    message = Column(String(255), nullable=False)
    request_date = Column(DateTime, default=Dates.UTCNow())
    aFrom = Column( Integer, ForeignKey('social_network.account.id'))
    aTo = Column(Integer, ForeignKey('social_network.account.id'))
    status = Column(String,
        ForeignKey('social_network.status.name'),
        nullable=False,
        default="QUEUED")
    UniqueConstraint(
        'aFrom',
        'aTo',
        name='unique_invitation')
        
    

    def __init__(self, aFrom, aTo, mess):
        self.aFrom = aFrom
        self.aTo = aTo
        self.message = mess

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Account, self).save(force_insert, force_update)
