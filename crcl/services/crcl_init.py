# -*- coding: utf-8 -*-
import httplib

from zato.server.service import Service

from crcl.models import city, country, language, region
from crcl.resources import config

from commons.base import Base


"""  """
class Generate(Service):
    class SimpleIO:
        output_required = ('result',)

    def handle(self):

        try:
            session = self.outgoing.sql.get('crcl').session()
            engine = session.get_bind()

            TablesToCreate = [
                city.City.__table__, 
                language.Language.__table__, 
                country.Country.__table__,
                country.Country.association_table,
                region.Region.__table__
            ]

            Base.metadata.create_all(engine, tables=TablesToCreate, checkfirst=True)

            fake_conn = engine.raw_connection()
            fake_cur = fake_conn.cursor()

            dbcopy_f = open(config['sql']['countries'], 'rb')

            copy_sql = "COPY crcl.country FROM STDOUT WITH CSV HEADER DELIMITER ','"
            fake_cur.copy_expert(copy_sql, dbcopy_f)
            
            dbcopy_f = open(config['sql']['regions'], 'rb')

            copy_sql = "COPY crcl.region FROM STDOUT WITH CSV HEADER DELIMITER ','"

            fake_cur.copy_expert(copy_sql, dbcopy_f)
            dbcopy_f = open(config['sql']['cities'], 'rb')

            copy_sql = "COPY crcl.city FROM STDOUT WITH CSV HEADER DELIMITER ','"
            fake_cur.copy_expert(copy_sql, dbcopy_f)

            dbcopy_f = open(config['sql']['languages'], 'rb')

            copy_sql = "COPY crcl.language FROM STDOUT WITH CSV HEADER DELIMITER ','"
            fake_cur.copy_expert(copy_sql, dbcopy_f)

            dbcopy_f = open(config['sql']['country_languages'], 'rb')

            copy_sql = "COPY crcl.rel_country_language FROM STDOUT WITH CSV HEADER DELIMITER ','"
            fake_cur.copy_expert(copy_sql, dbcopy_f)

            fake_conn.commit()
            fake_cur.close()

            session.close()

            parameters = {'data_format':'json'}
            self.response.payload.result = True


        except Exception, e:
            session.close()
            self.logger.error(e)
            self.response.status_code = httplib.INTERNAL_SERVER_ERROR
            self.response.payload.result = False

    

class Drop(Service):
    class SimpleIO:
        output_required = ('result',)

    def handle(self):

        try:
            session = self.outgoing.sql.get('crcl').session()
            self.engine = session.get_bind()

            TablesToDrop = [
                city.City.__table__, 
                language.Language.__table__, 
                country.Country.__table__,
                country.Country.association_table,
                region.Region.__table__
            ]

            Base.metadata.drop_all(self.engine, tables=TablesToDrop, checkfirst=True)

            session.close()

            parameters = {'data_format':'json'}
            self.response.payload.result =  True
        except Exception, e:
            self.logger.error(e)
            self.response.status_code = httplib.INTERNAL_SERVER_ERROR
            self.response.payload.result = False
