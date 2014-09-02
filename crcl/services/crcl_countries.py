# -*- coding: utf-8 -*-
import httplib

from zato.server.service import Service
from zato.common import DATA_FORMAT
from json import dumps, loads

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from contextlib import closing

from crcl.models.country import Country
from crcl.models.language import Language
from crcl.models.region import Region
from crcl.models.city import City


class getCountries(Service):
    class SimpleIO:
        output_required = ('result',) 
    def handle(self):
        dbName = "crcl"
        with closing(self.outgoing.sql.get(dbName).session()) as session:
            try:
                self.response.payload.result = \
                    session.execute('SELECT * FROM crcl.country')
            except Exception, e:
                self.logger.error("Error getCountries:28", e)
                self.response.status_code = httplib.INTERNAL_SERVER_ERROR
                self.response.payload.result = False


class getCountry(Service):
    class SimpleIO:
        input_optional = ('id', 'name',)
        output_required = ('result',)
    def handle(self):
        from urlparse import parse_qs

        qs = parse_qs(self.wsgi_environ['QUERY_STRING'])

        dbName = "crcl"


        if 'id' in qs.keys():
            with closing(self.outgoing.sql.get(dbName).session()) as session:
                try:
                    result = (session.query(Country).\
                            filter(Country.id == qs['id'][0])).one()
                    self.response.payload.result = result.toJSON()
                except Exception, e:
                    self.response.status_code = httplib.INTERNAL_SERVER_ERROR
                    self.response.payload.result = False
        elif 'name' in qs.keys():
            with closing(self.outgoing.sql.get('crcl').session()) as session:
                try:
                    result = (session.query(Country).\
                            filter(Country.name == qs['name'][0])).one()
                    self.response.payload.result = result.toJSON()
                except Exception, e:
                    self.response.status_code = httplib.INTERNAL_SERVER_ERROR
                    self.response.payload.result = False 
        else:
            self.response.status_code = httplib.INTERNAL_SERVER_ERROR
            self.response.payload.result = False

class getCountryLanguages(Service):
    class SimpleIO:
        input_optional = ('id', 'name',)
        output_required = ('result',)
    def handle(self):

        from urlparse import parse_qs

        qs = parse_qs(self.wsgi_environ['QUERY_STRING'])

        dbName = "crcl"

        if 'id' in qs.keys():
            self.logger.info(qs['id'][0])
            with closing(self.outgoing.sql.get(dbName).session()) as session:
                try:
                    results = (session.query(Language).join(Language.countries).\
                            filter(Country.id == qs['id'][0])).all()
                    self.response.payload.result = [obj.toJSON() for obj in results]
                except Exception, e:
                    self.response.status_code = httplib.INTERNAL_SERVER_ERROR
                    self.response.payload.result = False
        elif 'name' in qs.keys():
            with closing(self.outgoing.sql.get('crcl').session()) as session:
                try:
                    results = (session.query(Language).join(Language.countries).\
                            filter(Country.name == qs['name'][0])).all()

                    self.response.payload.result = [obj.toJSON() for obj in results]
                except Exception, e:
                    self.response.status_code = httplib.INTERNAL_SERVER_ERROR
                    self.response.payload.result = False 
        else:
            self.response.status_code = httplib.INTERNAL_SERVER_ERROR
            self.response.payload.result = False


class getCountryRegions(Service):
    class SimpleIO:
        input_optional = ('id', 'name',)
        output_required = ('result',)
    def handle(self):

        from urlparse import parse_qs

        qs = parse_qs(self.wsgi_environ['QUERY_STRING'])

        dbName = "crcl"

        if 'id' in qs.keys():
            self.logger.info(qs['id'][0])
            with closing(self.outgoing.sql.get(dbName).session()) as session:
                try:
                    results = (session.query(Region).join(Region.country).\
                            filter(Country.id == qs['id'][0])).all()
                    self.logger.info(results)
                    self.response.payload.result = [obj.toJSON() for obj in results]
                except Exception, e:
                    self.logger.error(e)
                    self.response.status_code = httplib.INTERNAL_SERVER_ERROR
                    self.response.payload.result = False
        elif 'name' in qs.keys():
            with closing(self.outgoing.sql.get('crcl').session()) as session:
                try:
                    results = (session.query(Region).join(Region.country).\
                            filter(Country.name == qs['name'][0])).all()

                    self.response.payload.result = [obj.toJSON() for obj in results]
                except Exception, e:
                    self.logger.error(e)
                    self.response.status_code = httplib.INTERNAL_SERVER_ERROR
                    self.response.payload.result = False 
        else:
            self.response.status_code = httplib.INTERNAL_SERVER_ERROR
            self.response.payload.result = False


class getCountryCities(Service):
    class SimpleIO:
        input_optional = ('id', 'name',)
        output_required = ('result',)
    def handle(self):

        from urlparse import parse_qs

        qs = parse_qs(self.wsgi_environ['QUERY_STRING'])

        dbName = "crcl"

        if 'id' in qs.keys():
            self.logger.info(qs['id'][0])
            with closing(self.outgoing.sql.get(dbName).session()) as session:
                try:
                    results = (session.query(City).\
                            filter(City.country_id_fk == qs['id'][0])).all()
                    self.response.payload.result = [obj.toJSON() for obj in results]
                except Exception, e:
                    self.logger.error(e)
                    self.response.status_code = httplib.INTERNAL_SERVER_ERROR
                    self.response.payload.result = False
        elif 'name' in qs.keys():
            with closing(self.outgoing.sql.get('crcl').session()) as session:
                try:
                    results = (session.query(City).\
                            join(Country, City.country_id_fk == Country.id).\
                            filter(Country.name == qs['name'][0])).all()
                    self.logger.info([obj.toJSON() for obj in results])
                    self.response.payload.result = [obj.toJSON() for obj in results]
                except Exception, e:
                    self.logger.error(e)
                    self.response.status_code = httplib.INTERNAL_SERVER_ERROR
                    self.response.payload.result = False 
        else:
            self.response.status_code = httplib.INTERNAL_SERVER_ERROR
            self.response.payload.result = False