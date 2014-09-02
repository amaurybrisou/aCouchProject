# -*- coding: utf-8 -*-
import httplib

from zato.server.service import Service
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from contextlib import closing

from social_network.models import account, address, comment, deletion, deletion_reason, email, invitation, page, post, status

from commons.base import Base

from social_network.resources import config

"""  """
class Generate(Service):
    class SimpleIO:
        output_required = ('result',)

    def handle(self):

        try:
            ret = self.invoke(
                'crcl-init.generate'
            )
            if not ret:
                raise Exception(ret)

            session = self.outgoing.sql.get('social_network').session()
            engine = session.get_bind()

            fake_conn = engine.raw_connection()
            fake_cur = fake_conn.cursor()

            TablesToCreate = [
                account.Account.__table__,
                account.Account.association_table_pages,
                account.Account.association_table_invitations,
                account.Account.association_table_friends,
                account.Account.association_table_languages,

                address.Address.__table__,
                comment.Comment.__table__,

                deletion_reason.Deletion_Reason.__table__,
                deletion.Deletion.__table__,
                
                email.Email.__table__,
                invitation.Invitation.__table__,
                
                page.Page.association_table_posts,
                page.Page.__table__,
                

                post.Post.__table__,
                status.Status.__table__,
            ]

            Base.metadata.create_all(engine, tables=TablesToCreate, checkfirst=True)

            dbcopy_f = open(config['sql']['deletion_reasons'], 'rb')

            copy_sql = "COPY social_network.deletion_reason FROM STDOUT WITH CSV HEADER DELIMITER ','"
            fake_cur.copy_expert(copy_sql, dbcopy_f)

            dbcopy_f = open(config['sql']['status'], 'rb')

            copy_sql = "COPY social_network.status FROM STDOUT WITH CSV HEADER DELIMITER ','"
            fake_cur.copy_expert(copy_sql, dbcopy_f)



            fake_conn.commit()
            fake_cur.close()

            session.close()

            self.response.payload.result =  True
        except Exception, e:
            self.logger.error(e)
            self.response.status_code = httplib.INTERNAL_SERVER_ERROR
            self.response.payload.result = False
    

class Drop(Service):
    class SimpleIO:
        output_required = ('result',)

    def handle(self):

        try:
            

            session = self.outgoing.sql.get('social_network').session()
            self.engine = session.get_bind()

            TablesToDrop = [
                account.Account.__table__,
                account.Account.association_table_pages,
                account.Account.association_table_invitations,
                account.Account.association_table_friends,
                account.Account.association_table_languages,

                address.Address.__table__,
                comment.Comment.__table__,
                deletion.Deletion.__table__,
                deletion_reason.Deletion_Reason.__table__,
                email.Email.__table__,
                invitation.Invitation.__table__,
                
                page.Page.__table__,
                page.Page.association_table_posts,

                post.Post.__table__,
                status.Status.__table__,
            ]

            Base.metadata.drop_all(self.engine, tables=TablesToDrop, checkfirst=True)

            session.close()

            ret = self.invoke(
                'crcl-init.drop'
            )
            if not ret:
                raise Exception(ret)

            parameters = {'data_format':'json'}
            self.response.payload.result =  True

        except Exception, e:
            self.logger.error(e)
            self.response.status_code = httplib.INTERNAL_SERVER_ERROR
            self.response.payload.result = False