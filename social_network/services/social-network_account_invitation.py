# -*- coding: utf-8 -*-

from contextlib import closing

from zato.server.service import Service, Boolean

from commons.util.dates import Dates

from social_network.models.account import Account
from social_network.models.invitation import Invitation

class Send(Service):
    class SimpleIO:
        input_required = ("aFromId", "aToId", "message" )
        output_required = ("status",)

    def handle(self):
        aFromId = self.request.input.aFromId
        aToId = self.request.input.aToId
        message = self.request.input.message

        out_name = "aCouch"
        with closing(self.outgoing.sql.get(out_name).session()) as session:
            try:
                aFrom_obj = session.query(Account). \
                    filter(Account.id == aFromId).one()
                aTo_obj = session.query(Account). \
                    filter(Account.id == aToId).one()
            except Exception, e:
                self.logger.error(e)
                self.response.payload.status = "No Such Account"
            try:
                invit = (session.query(Invitation).\
                    filter(Invitation.aFrom == aFrom_obj.id). \
                    filter(Invitation.aTo == aTo_obj.id)).one()
                if invit:
                    if invit.status in ("BLOCKED", "REJECTED",):
                        self.response.payload.status = invit.status
                    else:
                        self.response.payload.status = "Invitation already exist"
                    return
            except Exception, e:
                self.logger.warn(e)
            try:
                invit = Invitation(aFrom_obj.id, aTo_obj.id, message)

                session.add(invit)
                session.flush()

                aFrom_obj.invitations_to.append(invit)
                aTo_obj.invitations_from.append(invit)

                session.commit()

                self.response.payload.status = invit.status
            except Exception, e:
                self.logger.error(e)
                self.response.payload.status = -1

class ChangeStatus(Service):
    class SimpleIO:
        input_required = ("invitationId", "status")
        output_required = ("status",)

    def handle(self):
        invitationId = self.request.input.invitationId
        status = self.request.input.status

        out_name = "aCouch"
        with closing(self.outgoing.sql.get(out_name).session()) as session:
            try:
                invit = (session.query(Invitation).\
                    filter(Invitation.id == invitationId)).one()
                if not invit:
                    raise Exception("No Such Record", -18900)
            except Exception, e:
                self.logger.error(e)
                self.response.payload.status = e
            try:
                invit.status = status
                session.commit()

                from zato.common import DATA_FORMAT
                if status in { "ACCEPTED" }:
                    
                    ret = self.invoke_async(
                        'a-couch-account.add-friends',
                        {   "aFromId" : invit.aFrom,
                            "aToId" : invit.aTo },
                        data_format=DATA_FORMAT.JSON
                    )
                    if not ret:
                        raise Exception(ret)
                else:
                    ret = self.invoke_async(
                        'a-couch-account.remove-friends',
                        {   "aFromId" : invit.aFrom,
                            "aToId" : invit.aTo },
                        data_format=DATA_FORMAT.JSON
                    )
                    if not ret:
                        raise Exception(ret)

                self.response.payload.status = invit.status
            except Exception, e:
                self.logger.error(e)
                self.response.payload.status = -1