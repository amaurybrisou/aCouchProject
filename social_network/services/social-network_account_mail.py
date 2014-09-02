# -*- coding: utf-8 -*-

import httplib

from zato.server.service import Service
from commons.util import mail
from social_network.resources import config

class Send(Service):

    class SimpleIO:
        input_required = ('MailTo', 'subject', 'message' )
        output_required = ('result',)
        
    def handle(self):

        from commons.util.validator import Validator as v


        try:
            ret = mail.Send(from_addr=config['mail'],
                to_addr_list=self.request.input.MailTo,
                subject=self.request.input.subject,
                message=self.request.input.message,
                login=config['smtp']['username'], 
                password=config['smtp']['pasword']
                smtpserver=config['smtp']['addr'])
            self.logger.info("Mail Sent "+unicode(ret))
        except Exception, e:
            self.logger.error(e)
            self.response.status_code = httplib.INTERNAL_SERVER_ERROR
            self.response.payload.result = False