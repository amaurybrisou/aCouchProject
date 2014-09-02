# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Table, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from commons.util.dates import Dates

from social_network.models.post import Post

from commons.base import Base



# Create your models here.
class Page(Base):
    __table_args__ = { 'schema': 'social_network'}

    id = Column(Integer, primary_key=True)
    link = Column(String(128), nullable=False, unique=True)
    title = Column(String(128))
    body = Column(String)
    creation_date = Column(DateTime, default=Dates.UTCNow())
    
    
    association_table_posts = Table('rel_pages_posts', Base.metadata, 
        Column('post_id_fk', Integer, ForeignKey('social_network.post.id'),
            primary_key=True),
        Column('page_id_fk', Integer, ForeignKey('social_network.page.id'),
            primary_key=True),
        schema='social_network',
    )
    posts = relationship("Post",
        secondary=association_table_posts,
        backref="pages")



    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Page, self).save(force_insert, force_update)