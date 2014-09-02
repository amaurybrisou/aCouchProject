# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from commons.util.dates import Dates

from social_network.models.comment import Comment

from commons.base import Base



# Create your models here.
class Post(Base):
    __table_args__ = { 'schema': 'social_network'}
		
    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, default=Dates.UTCNow())
    title = Column(String(128), nullable=False)
    content = Column(String(500))
    comments = relationship("Comment", backref="post")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Post, self).save(force_insert, force_update)