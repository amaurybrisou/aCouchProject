# -*- coding: utf-8 -*-

from zato.server.service import Service

from couch_surfing.models import activity, couch, geo_loc, matrice, matrice_type, option

from commons.base import Base

"""  """
class GenerateCouchSurfing(Service):
    class SimpleIO:
        output_required = ('result',)

    def handle(self):


        session = self.outgoing.sql.get('aCouch').session()
        engine = session.get_bind()

        Base.metadata.create_all(engine, checkfirst=True)

        # fake_conn = engine.raw_connection()
        # fake_cur = fake_conn.cursor()

        # dbcopy_f = open(config['sql']['countries'], 'rb')

        # copy_sql = "COPY countries FROM STDOUT WITH CSV HEADER DELIMITER ','"
        # fake_cur.copy_expert(copy_sql, dbcopy_f)

        # fake_conn.commit()
        # fake_cur.close()

        session.close()

        self.response.payload.result =  'Couch-Surfing Generated'

    

class DropCouchSurfing(Service):
    class SimpleIO:
        output_required = ('result',)

    def handle(self):

        session = self.outgoing.sql.get('aCouch').session()
        self.engine = session.get_bind()

        Base.metadata.drop_all(self.engine, checkfirst=True)

        session.close()

        parameters = {'data_format':'json'}
        self.response.payload.result =  'Couch-Surfing Database Dropped'
