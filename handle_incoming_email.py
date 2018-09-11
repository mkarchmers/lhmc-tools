#
import webapp2
import hashlib as hs
import datetime
import re

from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext import ndb

import models


class InboundEmailHandler(InboundMailHandler):

    def get_hash(self, email):

        email = re.sub(r'.*<','',email)
        email = re.sub(r'>','',email)
        candidate_hash = hs.md5(email).hexdigest()
        key = ndb.Key(models.EmailHash, candidate_hash)

        return key.get()

    def find_patient(self, uid, patient_name):

        query = models.Patient.query(ancestor=models.UserKey.get(uid))

        res = [x for x in query.fetch() if x.name == patient_name]

        if len(res) > 0:
            return res[0]

        return None

    def find_latest_session(self, uid, patient_id):

        query = models.Session.query(ancestor=models.UserKey.get(uid))
        query = query.order(-models.Session.date_object)
        query = query.filter(models.Session.patient_id == patient_id)

        res = list(query.fetch(limit=1))

        if len(res) > 0:
            return res[0]

        return None

    def prepare(self, sender, subject, plaintext):

        parms = subject.split("ON")
        patient_name = parms.pop(0).strip()
        date = parms.pop(0).strip() if len(parms)>0 else None

        date_object = None
        try:
            date_object = datetime.datetime.strptime(date, '%m/%d/%Y').date()
        except:
            pass

        if patient_name == "":
            body = "Subject must contain a patient name.\n"
            return (None, body)

        if date_object is None:
            body = "Subject must specify a valid date (%s).\n"%date
            return (None, body)
        if date_object > datetime.date.today():
            body = "Cannot add session for a day in the future (%s)."%date
            return (None,body)


        hash = self.get_hash(sender)
        if hash is None:
            body = "User %s not permissioned.\n"%sender
            return (None, body)

        patient = self.find_patient(hash.uid, patient_name)
        if patient is None:
            body = "patient %s not found.\n"%patient_name        
            return (None, body)
        if patient.status != 'Active':
            body = "cannot add session for inactive patient.\n"
            return (None, body)

        pid = patient.key.urlsafe()

        latest = self.find_latest_session(hash.uid, pid)

        if latest is None:
            body = "This would be the first session for patient %s.\n"%patient_name
            body += "\nFirst session cannot be created via email.\n"
            return (None, body)

        if date_object <= latest.date_object:
            body = "Attempting to create a new session for %s.\n"%patient_name
            body += "New session date (%s) is on or prior to latest session on %s.\n"%(date_object, latest.date_object)
            return (None, body)

        new_session = models.Session(parent=models.UserKey.get(hash.uid), **latest.to_dict())

        new_session.date = date
        new_session.date_object = date_object

        new_session.timestamp = datetime.datetime.now()

        new_session.is_billed = False
        new_session.billing_time = None

        ndb.transaction(patient.increment)
        new_session.session_number = patient.session_number

        new_session.notes = "Client reported: " + plaintext if plaintext != "to-do" else "TODO"

        freq = latest.PLN_FREQ
        freq_map = {'Weekly': 7, 'Bi-weekly': 14, 'Monthly': 28}
        next_date = new_session.date_object + datetime.timedelta(days=freq_map[freq])
        new_session.PLN_NXT = next_date.strftime('%m/%d/%Y')

        body = "New session for %s on %s\n"%(patient_name, date)
        body += "Details:\n"
        body += "\tsession number: %i\n"%new_session.session_number
        body += "\tnext session planned for: %s\n"% new_session.PLN_NXT
        body += "\tnotes:\n\t%s\n"%new_session.notes

        return (new_session, body)

    def receive(self, mail_message):

        subject = ""
        try:
            subject = mail_message.subject
        except:
            pass
        user_mail = mail_message.sender

        plaintext_bodies = mail_message.bodies('text/plain')
        plaintext = 'empty'
        for content_type, body in plaintext_bodies:
            plaintext = body.decode()

        (session, body) = self.prepare(user_mail, subject, plaintext)
        if session is not None:
            session.put()

        sender = 'do-not-reply@{}.appspotmail.com'.format(app_identity.get_application_id())

        mail.send_mail(
                sender= sender,
                to= mail_message.sender,
                subject= "Re: email received on " + mail_message.date,
                body= body,
                )

# [START app]
app = webapp2.WSGIApplication([InboundEmailHandler.mapping()], debug=False)
# [END app]
