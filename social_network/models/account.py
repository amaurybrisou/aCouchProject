# -*- coding: utf-8 -*-

from sqlalchemy import Column, Table, Integer, Boolean,String, ForeignKey, ForeignKeyConstraint, DateTime
from sqlalchemy.orm import relationship, backref

import uuid
import hashlib

from crcl.models.language import Language

from social_network.models.deletion import Deletion
from social_network.models.invitation import Invitation
from social_network.models.page import Page

from commons.util.dates import Dates

from commons.base import Base


# Create your models here.
class Account(Base):
    __table_args__ = { 'schema': 'social_network'}

    def __init__(self, firstname, lastname, birthdate, password, personal_page=""):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.personal_page = personal_page
        self.password = hashlib.md5(password).hexdigest()
        self.token=unicode(uuid.uuid4())

    id = Column(Integer, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    birthdate = Column(DateTime)
    telephone = Column(String(50), nullable=True)
    password = Column(String(50), nullable=False)
    registered = Column(Integer, default=0)
    active = Column(Integer, default=1)
    type = Column(String)
    first_login_date = Column(DateTime, default=Dates.UTCNow())
    last_login_date = Column(DateTime)
    authenticated = Column(Boolean, default=False)
    token = Column(String, nullable=False)
    mail_id_fk = Column(Integer, ForeignKey('social_network.email.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    mail_sos_id_fk = Column(Integer, ForeignKey('social_network.email.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)


    association_table_pages = Table('rel_accounts_pages', Base.metadata,
        Column('account_id_fk', Integer, ForeignKey('social_network.account.id'),
            primary_key=True),
        Column('page_id_fk', Integer, ForeignKey('social_network.page.id'),
            primary_key=True),
        schema='social_network',
    )
    pages = relationship("Page",
        secondary=association_table_pages,
        backref="account")
    

    association_table_invitations = Table('rel_invitations', Base.metadata, 
        Column('account_id_fk', Integer, ForeignKey('social_network.account.id'),
            primary_key=True),
        Column('invitation_id_fk', Integer, ForeignKey('social_network.invitation.id'),
            primary_key=True),
        schema='social_network',
    )
    invitations_to = relationship("Invitation",
        secondary=association_table_invitations,
        backref="account_from")

    invitations_from = relationship("Invitation",
        secondary=association_table_invitations,
        backref="account_to")


    association_table_friends = Table('rel_friends', Base.metadata,
        Column('account_id_fk', Integer, ForeignKey('social_network.account.id'),
            primary_key=True),
        Column('friend_id_fk', Integer, ForeignKey('social_network.account.id'),
            primary_key=True),
        schema='social_network',
    )
    
    friends = relationship("Account",
                secondary=association_table_friends,
                backref='added_by',
                primaryjoin=id == association_table_friends.c.account_id_fk,
                secondaryjoin=id == association_table_friends.c.friend_id_fk
            )

    association_table_languages = Table('rel_accounts_languages', Base.metadata, 
        Column('account_id_fk',
            Integer,
            ForeignKey('social_network.account.id',
                onupdate="CASCADE",
                ondelete="CASCADE"),
            primary_key=True),
        Column('language_id_fk',
            Integer,
            ForeignKey('crcl.language.id',
                onupdate="CASCADE",
                ondelete="CASCADE"),
            primary_key=True),
        Column('skill', String(12)),
        schema='social_network',
    )
    languages = relationship("Language",
        secondary=association_table_languages,
        backref="accounts")

    deletion_id_fk = Column(Integer,
        ForeignKey('social_network.deletion.id',
            onupdate="CASCADE",
            ondelete="CASCADE"))
    deletion = relationship("Deletion", uselist=False)

    address_id_fk = Column(Integer, 
        ForeignKey('social_network.address.id'))