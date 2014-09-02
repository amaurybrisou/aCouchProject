# -*- coding: utf-8 -*-

from contextlib import closing

from zato.server.service import Service, Boolean

from commons.util.dates import Dates
from commons.util import mail

from social_network.models.email import Email
from social_network.models.page import Page
from social_network.models.deletion import Deletion
from social_network.models.address import Address
from social_network.models.account import Account

from crcl.models.language import Language
from crcl.models.city import City
from crcl.models.country import Country
from crcl.models.region import Region

from social_network.resources import config

from commons.util.validator import Validator as v


class Create(Service):
    class SimpleIO:
        input_required = ('firstname', 'city', 'lastname',
            'birthdate', 'password', 'language', 'country',
            'email', 'email_sos', 'street_number', 'street_name',)
        input_optional = ('telephone', 'registered',)
        output_required = ('result',)
        
    def handle(self):
        args = self.request.input

        out_name = 'social_network'
        firstname = args.firstname
        lastname = args.lastname
        birthdate = args.birthdate
        password = args.password
        # if not v.password(password):
        #     self.response.payload.result = "Invalid Password"
        #     return
        
        country = args.country
        language = args.language
        city = args.city
        email_address = args.email
        if not v.mail(email_address):
            self.response.payload.result = "Invalid Email Address"
            return
        email_address_sos = args.email_sos
        if not v.mail(email_address_sos):
            self.response.payload.result = "Invalid Sos Email Address"
            return

        street_number = args.street_number
        street_name = args.street_name
      
        email = Email(address=email_address)
        email_sos = Email(mail_type="sos", address=email_address_sos)
        address = Address(
            street_number=street_number,
            street_name=street_name
            )
        account = Account(
            firstname=firstname,
            lastname=lastname,
            birthdate=birthdate,
            password=password
            )
        page = Page(link="http://"+config['hostname']+\
                    ':'+unicode(config['ports']['http'])+\
                    config['api']['base_url']+\
                    '/'+firstname.lower()+'_'+\
                    lastname.lower())

        out_name = 'social_network'
        with closing(self.outgoing.sql.get(out_name).session()) as session:
            try:
                language = (session.query(Language).\
                    filter(Language.name == language)).one()
            except Exception, e:
                self.logger.warn(e)
                self.response.payload.result = "Language Doesn't exist"    
            
            try:
                country = (session.query(Countries). \
                    filter(Countries.name == country)).one()
            except Exception, e:
                self.logger.warn(e)
                self.response.payload.result = "Country Doesn't exist"    
            
            try:    
                city = (session.query(Cities). \
                    filter(Cities.name == city). \
                    filter(Cities.country_id_fk == country.id)).one()
            except Exception, e:
                self.logger.warn(e)
                self.response.payload.result = "City Doesn't exist"

            try:
                address = session.query(Address).\
                    filter(Address.street_name == street_name).\
                    filter(Address.street_number == street_number).\
                    filter(Address.city_id_fk == city.id).first()


                if not address:
                    address = Address(
                        street_number=street_number,
                        street_name=street_name
                    )
                    address.city_id_fk = city.id
                    session.add(address)
                    session.flush()

                #flush to get Ids Generated
                session.add(email)
                session.add(email_sos)
                session.add(page)
                session.flush()
                
                account.languages.append(language)
                
                account.address_id_fk = address.id
                account.mail_id_fk = email.id
                account.mail_sos_id_fk = email_sos.id
                account.pages.append(page)
                session.add(account)
                session.flush()

                session.commit()

                from zato.common import DATA_FORMAT
                ret = self.invoke(
                    'a-couch-account-mail.send',
                    {   "MailTo" : email.address,
                        "subject" : "Account Validation",
                        "message"  : config['api']['base_validation_url']+account.token
                    },
                    data_format=DATA_FORMAT.JSON
                )
                self.logger.warn(ret)
                if not ret:
                    raise Exception("Error Sending Validation Mail : "+ret)

            except Exception, e:
                session.rollback()
                self.logger.error("Error inserting new Account")
                self.logger.error(e)
                self.response.payload.result = e # "Error Inserting New Account"
                return
        self.response.payload.result = account.toJSON()

class GetById(Service):
    class SimpleIO:
        input_required = ('id', Boolean('force'))
        output_required = ('result',)

    def handle(self):
        account_id = self.request.input.id
        force = self.request.input.force
        out_name = 'social_network'

        parameters = {'data_format':'json'}
        with closing(self.outgoing.sql.get(out_name).session()) as session:
            try:
                a = (session.query(Account).\
                    filter(Account.id == account_id).one())
            
                if force:
                    self.response.payload.result = a.toJSON()
                else:
                    if not a.deletion_id_fk:
                        self.response.payload.result = a.toJSON()
                    else:
                        self.response.payload.result = \
                            "Account exist but schedule for deletion"        
            except Exception, e:
                self.logger.warn('Querying for unknown Account Id : ' \
                    +unicode(account_id))
                self.response.payload.result = "No Such Account"

class DeleteById(Service):
    class SimpleIO:
        input_required = ('id', 'deletion_reason_id')
        output_required = ('result',)

    def handle(self):
        account_id = self.request.input.id
        deletion_reason_id = self.request.input.deletion_reason_id
        out_name = 'social_network'

        parameters = {'data_format':'json'}
        
        deletion = Deletion(
            request_date=Dates.UTCNow(),
            effective_date=Dates.expirationDate(),
            deletion_reason_id_fk = deletion_reason_id)

        with closing(self.outgoing.sql.get(out_name).session()) as session:
            try:
                a = session.query(Account).filter(Account.id == account_id).one()

                session.add(deletion)
                session.flush()

                a.deletion_id_fk = deletion.id
                
                session.commit()
                self.response.payload.result = "Done"
            except Exception, e:
                self.logger.warn('Querying for unknown Account Id : ' \
                    +unicode(account_id))
                self.response.payload.result = "No Such Account"

class FullDeletion(Service):
    def handle(self):
        out_name = "social_network"
        with closing(self.outgoing.sql.get(out_name).session()) as session:
            try: 
                session.execute('SELECT * FROM status')
                session.commit()
            except Exception, e:
                self.logger.error(e)


class AddFriends(Service):
    class SimpleIO:
        input_required = ('aFromId', 'aToId')
        output_required = ('result',)

    def handle(self):
        aFromId = self.request.input.aFromId
        aToId = self.request.input.aToId
        out_name = "social_network"
        with closing(self.outgoing.sql.get(out_name).session()) as session:
            try: 
                aFrom_obj = (session.query(Account).\
                    filter(Account.id == aFromId)).one()
                aTo_obj = (session.query(Account).\
                    filter(Account.id == aToId)).one()
                if not aFrom_obj or not aTo_obj:
                    raise Exception('No such Account')
            except Exception, e:
                self.logger.error(e)
                self.response.payload.result = "Error Fetching Friends Accounts"
            try:
                aFrom_obj.friends.append(aTo_obj)
                aTo_obj.friends.append(aFrom_obj)
                session.commit()
                self.response.payload.result = 1
            except Exception, e:
                self.logger.error(e)
                self.response.payload.result = "Error Adding Friends"

class RemoveFriends(Service):
    class SimpleIO:
        input_required = ('aFromId', 'aToId')
        output_required = ('result',)

    def handle(self):
        aFromId = self.request.input.aFromId
        aToId = self.request.input.aToId
        out_name = "social_network"
        with closing(self.outgoing.sql.get(out_name).session()) as session:
            try: 
                aFrom_obj = (session.query(Account).\
                    filter(Account.id == aFromId)).one()
                aTo_obj = (session.query(Account).\
                    filter(Account.id == aToId)).one()
                if not aFrom_obj or not aTo_obj:
                    raise Exception('No such Account')
            except Exception, e:
                self.logger.error(e)
                self.response.payload.result = "Error Fetching Friends Accounts"
            try:
                aFrom_obj.friends.remove(aTo_obj)
                aTo_obj.friends.remove(aFrom_obj)
                session.commit()
                self.response.payload.result = 1
            except Exception, e:
                self.logger.error(e)
                self.response.payload.result = "Error Adding Friends"

class Validate(Service):
    class SimpleIO:
        input_required = ('token',)
        output_required = ('result',)

    def handle(self):
        from urlparse import parse_qs
        qs = parse_qs(self.wsgi_environ['QUERY_STRING'])
        token = qs['token'][0]

        out_name = "social_network"
        with closing(self.outgoing.sql.get(out_name).session()) as session:
            try:
                a = (session.query(Account).\
                    filter(Account.token == token)).one()
                if a:
                    a.registered = 1
                    session.commit()
                    self.response.payload.result = "Account registered"
                    return
                else:
                    self.response.payload.result = "Access Denied"
                    return
            except Exception, e:
                    self.logger.error(e)
                    self.response.payload.result = "Error"

class Authenticate(Service):
    class SimpleIO:
        input_required = ('password',)
        input_optional = ('email', 'name',)
        output_required = ('result',)

    def handle(self):
        email = self.request.input.email
        account_id = self.request.input.password
