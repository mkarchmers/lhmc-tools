import json
import jinja2
import webapp2
import os
import urllib
import urllib2
import logging
from google.appengine.ext import db
from datetime import datetime as dt
from datetime import date as d
import random as r
import hashlib as hs
from google.appengine.api import users
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def user_key(uid):
    """Constructs a Datastore key for a User entity.
    """
    return ndb.Key('User',uid)

class ModelEncoder(json.JSONEncoder):
    def default(self, obj): 

        if isinstance(obj, db.Model): 
            properties = obj.properties().items() 
            output = {} 
            for field, value in properties: 
                output[field] = getattr(obj, field) 
            return output 

        return json.JSONEncoder.default(self, obj) 


# for testing
class Test(ndb.Model):

    a = ndb.StringProperty(indexed=True)
    b = ndb.StringProperty(default='x', choices=['x','y'], indexed=False)
    c = ndb.StringProperty()
    d = ndb.DateProperty()

class TestHandler(webapp2.RequestHandler):

    def get(self):
        import datetime
        user = users.get_current_user()

        t = Test(parent=user_key(user.user_id()))
        t.a = self.request.get('a')
        t.d = datetime.datetime(2018,8,31)
        t.c = "first\nsecond"
        t.put()
        self.response.write("success")


class GetHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        greetings_query = Test.query(
            ancestor=user_key(user.user_id()))
        greetings = greetings_query.fetch(10)

        q = Test.query(ancestor=user_key(user.user_id()))
        q = q.filter(Test.a==unicode(self.request.get('a')))
        greetings = q.iter(limit=10)
        self.response.write(list(greetings))
# done testing    


class Patient(db.Model):

    fname = db.StringProperty(indexed=False)
    lname = db.StringProperty()
    dob = db.StringProperty(indexed=False)
    pid = db.StringProperty()
    insurance = db.StringProperty()
    session_number = db.IntegerProperty(indexed=False)
    user_id = db.StringProperty()

    def increment(self, amount=1):
        self.session_number += amount
        self.put()


class Session(db.Model):

    user_id = db.StringProperty()

    patient_id = db.StringProperty()
    session_id = db.StringProperty()
    is_billed = db.BooleanProperty()
    billing_time = db.DateTimeProperty()
    insurance = db.StringProperty()
    mod_code = db.StringProperty()

    session_number = db.IntegerProperty()

    date = db.StringProperty()
    date_object = db.DateProperty()
    timestamp = db.DateTimeProperty()

    fname = db.StringProperty()
    lname = db.StringProperty()
    dob = db.StringProperty()
    diag = db.StringProperty()
    diag_code = db.StringProperty()
    modality = db.StringProperty()
    new_issue = db.StringProperty()

    RA_none = db.StringProperty()
    RA_self_idea = db.StringProperty()
    RA_self_plan = db.StringProperty()
    RA_self_att = db.StringProperty()
    RA_others_idea = db.StringProperty()
    RA_others_plan = db.StringProperty()
    RA_others_att = db.StringProperty()
    RA_prop_idea = db.StringProperty()
    RA_prop_plan = db.StringProperty()
    RA_prop_att = db.StringProperty()
    TI_refl_listen = db.StringProperty()
    TI_encour = db.StringProperty()
    TI_decis_balnc = db.StringProperty()
    TI_prob_solv = db.StringProperty()
    TI_pos_reinforce = db.StringProperty()
    TI_explore = db.StringProperty()
    TI_play_therapy = db.StringProperty()
    TI_valid = db.StringProperty()
    TI_conf_behav = db.StringProperty()
    TI_real_test = db.StringProperty()
    TI_PSCR = db.StringProperty()
    TI_CSB = db.StringProperty()
    TI_PSB = db.StringProperty()
    TI_emot_supp = db.StringProperty()
    Other = db.StringProperty()

    notes = db.StringProperty(multiline=True)

    G_1_impr = db.StringProperty(indexed=False)


class Insurance(db.Model):

    name = db.StringProperty()
    mod_code = db.StringProperty()
    modality_of_session = db.StringProperty()


class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
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
        }

        template = JINJA_ENVIRONMENT.get_template('index2.html')
        self.response.write(template.render(template_values))


class EmailHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        email = "not logged in" if (user is None) else user.email()
        self.response.write(email)


class Insurance_init(webapp2.RequestHandler):

    def get(self):

        i = Insurance()
        i.name = "BlueCrossBlueShield"
        i.mod_code = "90846"
        i.modality_of_session = "Family without patient"
        i.put()
        i = Insurance()
        i.name = "BlueCrossBlueShield"
        i.mod_code = "90834"
        i.modality_of_session = "Individual"
        i.put()
        i = Insurance()
        i.name = "BlueCrossBlueShield"
        i.mod_code = "90847"
        i.modality_of_session = "Family with patient"
        i.put()
        self.response.write("done!")


class InsuranceHandler(webapp2.RequestHandler):
    def get(self):

        name = self.request.get('name')
        mod_code = self.request.get('modcode')
        modality_of_session = self.request.get('modsession')
        q = self.request.get('query')

        query = db.Query(Insurance)
        res = [{'Insurance': x.name, 'mod_code': x.mod_code, 'mod': x.modality_of_session} for x in
               query.run(limit=10)]
        obj = {'Insurance': res}
        if name is not '' and mod_code is not '' and modality_of_session is not '' and q is '':
            I = Insurance(name=name, mod_code=mod_code, modality_of_session=modality_of_session)
            I.put()

        if q is not '' and name is not '' and modality_of_session is not '':
            query.filter('name =', name)
            query.filter('modality_of_session =', modality_of_session)

            res = [{'mod_code': x.mod_code} for x in
                   query.run(limit=10)]
            obj = {'Insurance_code': res}

        self.response.write(json.dumps(obj))

        
class NS(webapp2.RequestHandler):

    def post(self):
        parms = {}
        for (k,v) in self.request.POST.items():
            parms[k] = v

        #self.response.write(parms)
        url = "/sessions?" + urllib.urlencode(parms)
        self.redirect(url)
        #self.redirect(url)

class PatientHandler(webapp2.RequestHandler):

    def post(self):
        user = users.get_current_user()

        parms = {}
        for (k,v) in self.request.POST.items():
            parms[k] = v
        parms['session_number'] = int(parms['session_number'] or "0")
        parms['user_id'] = user.user_id()
        parms['pid'] = str(hs.md5(parms['lname']))
        p = Patient(**parms)
        p.put()

        self.redirect('/')

    def get(self):

        user = users.get_current_user()
        uid = user.user_id()

        query = db.Query(Patient)
        query.filter('user_id =', uid)

        #s = [{'fname': x.fname, 'lname': x.lname, 'dob': x.dob, 'pid': x.pid,
        #      'insurance': x.insurance, 'session_number': x.session_number} for x in query.run()]
        s = list(query.run())
        obj = {'patient_list': s}

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(obj, cls=ModelEncoder))



class BillingHandler(webapp2.RequestHandler):

    def get(self):

    	user = users.get_current_user()
        uid = user.user_id()

        query = db.Query(Session)
        query.order('date_object')
        query.filter('is_billed =', False)
        query.filter('user_id = ', uid)
        #query.projection()

        res = [{'session_date': x.date, 'first': x.fname, 'last': x.lname, 'bill_code': x.mod_code,
                'diag_code': x.diag_code, 'insurance': x.insurance} for x in query.run()]


        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({'Bill': res}))

        if self.request.get('bill') is not '':
            bill_time = dt.now()
            for s in query.run():
                s.is_billed = True
                s.billing_time = bill_time
                s.put()


class SessionsHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        user = users.get_current_user()
        uid = user.user_id()

        attrbs = ['patient_id', 'date', 'fname', 'lname', 'dob', 'insurance','diag', 'diag_code','modality',
                  'new_issue', 'RA_none', 'RA_self_idea', 'RA_self_plan', 'RA_self_att', 'RA_others_idea',
                  'RA_others_plan', 'RA_others_att', 'RA_prop_idea',
                  'RA_prop_plan', 'RA_prop_att', 'TI_refl_listen',
                  'TI_encour', 'TI_decis_balnc', 'TI_prob_solv', 'TI_pos_reinforce', 'TI_explore', 'TI_play_therapy',
                  'TI_valid', 'TI_conf_behav', 'TI_real_test', 'TI_PSCR', 'TI_CSB', 'TI_PSB', 'TI_emot_supp', 'Other',
                  'user_id', 'notes', 'G_1_impr']

        new_sess = {}
        for att in attrbs:
            val = self.request.get(att)
            new_sess[att] = val

        # get mode code
        if new_sess['date'] is not '':
            query = db.Query(Insurance)
        	# print new_sess['insurance']
        	# print new_sess['modality_of_session']
            query.filter('name =', new_sess['insurance'])
            query.filter('modality_of_session =', new_sess['modality'])
            res = [{'mod_code': x.mod_code} for x in
                   query.run(limit=1)][0]
            new_sess['mod_code'] = res['mod_code']
            new_sess['is_billed'] = False

            user_date_lst = new_sess['date'].split('/')
            new_sess['date_object'] = d(int(user_date_lst[2]), int(user_date_lst[0]), int(user_date_lst[1]))
            new_sess['timestamp'] = dt.now()
            new_sess['session_id'] = str(r.randint(0, 10000000000))

            query = db.Query(Patient)
            query.filter('pid =', new_sess['patient_id'])
            patient = [x for x in query.run(limit=1)][0]
            db.run_in_transaction(patient.increment, 1)
            new_sess['session_number'] = patient.session_number

            new_sess['user_id'] = uid

            session = Session(**new_sess)
            session.put()

        query = db.Query(Session)
        query.order('-date_object')

        # %m%d%y

        pid = self.request.get('pid')


        s = [{'fname': x.fname, 'lname': x.lname, 'session_date': x.date_object, 'session_id': x.session_id,
              'timestamp': x.timestamp,'pid': x.patient_id, 'uid': x.user_id,
              'data': vars(x)['_entity']} for x in query.run(limit=100)]

        relevant = [x for x in s if x['pid'] == pid and x['uid'] == uid]
        if len(relevant) > 0:
            obj = {'relevant_list': relevant, 'latest_relevant': (lambda x: relevant[0] if len(relevant) > 0 else '')(0)}
        else:
            obj = {'patient_list': s, 'relevant_list': relevant,
                   'latest_relevant': (lambda x: relevant[0] if len(relevant) > 0 else '')(0)}

        self.response.write(json.dumps(obj, default=str))
