# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from commons.util.dates import Dates

from commons.base import Base



# Create your models here.
class Comment(Base):
    __table_args__ = { 'schema': 'social_network'}

    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, default=Dates.UTCNow())
    title = Column(String(128), nullable=False)
    subject = Column(String(128))
    content = Column(String(128))
    cFrom = Column(Integer, ForeignKey('social_network.account.id'))
    post_id_fk = Column(Integer, ForeignKey('social_network.post.id'))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Comment, self).save(force_insert, force_update)