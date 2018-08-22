import json
import jinja2
import webapp2
import os
import urllib
import urllib2
import datetime
import hashlib as hs
from google.appengine.api import users
from google.appengine.ext import ndb

from lmhc import models


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):


    def get(self):
        user = users.get_current_user()

        permitted = models.EmailHash.validate(user.email())

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'logout'
            
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'permission': permitted
        }
        
        template = JINJA_ENVIRONMENT.get_template('index2.html')
        self.response.write(template.render(template_values))


class EmailHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        email = "not logged in" if (user is None) else user.email()

        candidate_hash = hs.md5(email.lower()).hexdigest()
        key = ndb.Key(models.EmailHash, candidate_hash)

        hash = key.get()

        if hash is None:
            self.response.write("failed")
            return

        hash.uid = str(user.user_id())
        hash.put()

        self.response.write("<p>%s</p><p>%s</p>"%(user.email(), user.user_id()))


class Permissions_init(webapp2.RequestHandler):

    def get(self):

        ident = '361e54ab7e96f7610187da7ba3691184'
        eh = models.EmailHash(id = ident)
        eh.Hash = ident
        eh.put()
        ident = 'bdb63475a053e834d0fd1a1d93d5034e'
        eh = models.EmailHash(id = ident)
        eh.Hash = ident
        eh.put()
        ident = '6215d7ccc7413110ea60829fb1284565'
        eh = models.EmailHash(id = ident)
        eh.Hash = ident
        eh.put()
        ident = 'd980f0ec1b5d23bd04ed702536e4b90f'
        eh = models.EmailHash(id = ident)
        eh.Hash = ident
        eh.put()
        self.response.write("done!")


class Insurance_init(webapp2.RequestHandler):

    def get(self):

        i = models.Insurance()
        i.name = "BlueCrossBlueShield"
        i.mod_code = "90846"
        i.modality_of_session = "Family without patient"
        i.put()
        i = models.Insurance()
        i.name = "BlueCrossBlueShield"
        i.mod_code = "90834"
        i.modality_of_session = "Individual"
        i.put()
        i = models.Insurance()
        i.name = "BlueCrossBlueShield"
        i.mod_code = "90847"
        i.modality_of_session = "Family with patient"
        i.put()
        i = models.Insurance()
        i.name = "BlueCrossBlueShield"
        i.mod_code = "90853"
        i.modality_of_session = "Group"
        i.put()
        i = models.Insurance()
        i.name = "BlueCrossBlueShield"
        i.mod_code = "90791"
        i.modality_of_session = "Evaluation"
        i.put()
        self.response.write("done!")

        
class PatientHandler(webapp2.RequestHandler):

    def post(self):
        user = users.get_current_user()

        parms = {}
        for (k,v) in self.request.POST.items():
            parms[k] = v
        parms['session_number'] = int(parms['session_number'] or "0")
        parms['parent'] = models.UserKey.get(user.user_id())
        p = models.Patient(**parms)
        p.put()

        self.redirect('/')

    def get(self):

        user = users.get_current_user()
        uid = user.user_id()

        query = models.Patient.query(ancestor=models.UserKey.get(uid))

        s = list(query.fetch())
        obj = {'patient_list': s}

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(obj, cls=models.ModelEncoder))


class BillingHandler(webapp2.RequestHandler):

    def get(self):

    	user = users.get_current_user()
        uid = user.user_id()

        query = models.Session.query(ancestor=models.UserKey.get(uid))
        query = query.order(models.Session.insurance)
        query = query.filter(models.Session.insurance != 'None')
        query = query.filter(models.Session.is_billed == False)
        query = query.order(models.Session.name)

        res = [{'session_date': x.date, 'name': x.name, 'bill_code': x.mod_code,
                'diag_code': x.diag_code, 'insurance': x.insurance} for x in query.fetch()]

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({'Bill': res}))

        if self.request.get('bill') == "Y":
            bill_time = datetime.datetime.now()
            for s in query.fetch():
                s.is_billed = True
                s.billing_time = bill_time
                s.put()


class SessionsHandler(webapp2.RequestHandler):

    def post(self):
        user = users.get_current_user()
        uid = user.user_id()

        parms = {}
        for (k,v) in self.request.POST.items():
            parms[k] = v

        session_id = parms.get('session_id', None)

        del parms['session_id']
        del parms['seshNo']

        if parms['insurance'] != 'None':
            parms['mod_code'] = models.Insurance.get_code(parms['insurance'], parms['modality'])
        else:
            parms['mod_code'] = 'None'

        user_date_lst = parms['date'].split('/')
        parms['date_object'] = datetime.date(int(user_date_lst[2]), int(user_date_lst[0]), int(user_date_lst[1]))
        parms['timestamp'] = datetime.datetime.now()

        if session_id is None or session_id == "":
            # new session
            # increment number of sessions for patient
            key = ndb.Key(urlsafe=parms['patient_id'])
            patient = key.get()
            ndb.transaction(patient.increment)
            parms['session_number'] = patient.session_number

            parms['is_billed'] = False

            parms['parent'] = models.UserKey.get(user.user_id())
            
            session = models.Session(**parms)
            session.put()
        else:
            # edit session
            key = ndb.Key(urlsafe=session_id)
            session = key.get()

            # reset attributes that are not in parms
            # these have values of "on"
            for k in session._properties.keys():
                v = getattr(session, k)
                if v is None:
                    continue
                if v == "on" and k not in parms:
                    setattr(session, k, None)

            # set new attributes
            for k,v in parms.iteritems():
                print k
                setattr(session, k, v)

            session.put()

        self.redirect('/')

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        user = users.get_current_user()
        uid = user.user_id()

        query = models.Session.query(ancestor=models.UserKey.get(uid))

        query = query.order(-models.Session.date_object)

        pid = self.request.get('pid')

        if pid !=  "" or pid:
            query = query.filter(models.Session.patient_id == pid)

        obj = list(query.fetch(limit=200))

        self.response.write(json.dumps(obj, cls=models.ModelEncoder))


class ScheduleHandler(webapp2.RequestHandler):

    def post(self):
        user = users.get_current_user()
        uid = user.user_id()

        clear = self.request.get('clear',False)
        if clear:
            ndb.delete_multi(
               models.Schedule.query(ancestor=models.UserKey.get(uid)).fetch(keys_only=True)
            )
            self.response.write('cleared')
            return

        parms = {}
        for (k,v) in self.request.POST.items():
            parms[k] = v
        parms['parent'] = models.UserKey.get(uid)
        p = models.Schedule(**parms)
        p.put()
        self.response.write('ok')

    def get(self):

        user = users.get_current_user()
        uid = user.user_id()

        query = models.Schedule.query(ancestor=models.UserKey.get(uid))

        obj = list(query.fetch(limit=200))

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(obj, cls=models.ModelEncoder))

class Test(webapp2.RequestHandler):

    def get(self):

        from cStringIO import StringIO
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        pdfFile = StringIO()

        x = 50
        y = 750
        c = canvas.Canvas(pdfFile, encrypt="mk")
        c.drawString(x*5,y,"Output")
        c.line(x,y-10,x*11,y-10)
        c.save()

        self.response.headers['content-type'] = 'application/pdf'
        self.response.headers['Content-Disposition'] = 'attachment; filename=file.pdf'
        self.response.out.write(pdfFile.getvalue())
         
