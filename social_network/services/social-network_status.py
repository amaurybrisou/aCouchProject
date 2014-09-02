# -*- coding: utf-8 -*-
import httplib

from zato.server.service import Service
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from contextlib import closing

from social_network.models.status import Status 

class getStatus(Service):
    class SimpleIO:
        output_required = ('result',) 
    def handle(self):
        out_name = "social_network"
        with closing(self.outgoing.sql.get(out_name).session()) as session:
            try: 
                self.response.payload.result = [obj.toJSON() for obj in session.query(Status).all()]
                
            except Exception, e:
                self.logger.error(e)
                self.response.status_code = httplib.INTERNAL_SERVER_ERROR
            	self.response.payload.result = False
