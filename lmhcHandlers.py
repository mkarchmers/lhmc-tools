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

	ASS_ABLE= db.StringProperty()
	ASS_CONST= db.StringProperty()
	ASS_COOP= db.StringProperty()
	ASS_EFFRT= db.StringProperty()
	ASS_INSIG= db.StringProperty()
	ASS_OR= db.StringProperty()
	ASS_other_txt= db.StringProperty()
	ASS_present= db.StringProperty()
	ASS_present_txt= db.StringProperty()
	G_1_decr= db.StringProperty()
	G_1_decr_txt= db.StringProperty()
	G_1_impr= db.StringProperty()
	G_1_impr_txt= db.StringProperty()
	G_2_decr= db.StringProperty()
	G_2_decr_txt= db.StringProperty()
	G_2_impr= db.StringProperty()
	G_2_impr_txt= db.StringProperty()
	G_cop_skills= db.StringProperty()
	G_expr= db.StringProperty()
	G_id_res= db.StringProperty()
	G_other_txt= db.StringProperty()
	G_sc_skills= db.StringProperty()
	G_verb= db.StringProperty()
	PLN_CONT= db.StringProperty()
	PLN_FREQ= db.StringProperty()
	PLN_NXT= db.StringProperty()
	PLN_PSY= db.StringProperty()
	PLN_other_txt= db.StringProperty()
	RA_none= db.StringProperty()
	RA_others_att= db.StringProperty()
	RA_others_idea= db.StringProperty()
	RA_others_plan= db.StringProperty()
	RA_prop_att= db.StringProperty()
	RA_prop_idea= db.StringProperty()
	RA_prop_plan= db.StringProperty()
	RA_self_att= db.StringProperty()
	RA_self_idea= db.StringProperty()
	RA_self_plan= db.StringProperty()
	SPA_ACTOUT= db.StringProperty()
	SPA_AGI= db.StringProperty()
	SPA_AHA= db.StringProperty()
	SPA_ALCHUSE= db.StringProperty()
	SPA_ANG= db.StringProperty()
	SPA_ARG= db.StringProperty()
	SPA_AX= db.StringProperty()
	SPA_DIFTRAN= db.StringProperty()
	SPA_DIT= db.StringProperty()
	SPA_DM= db.StringProperty()
	SPA_DRGUSE= db.StringProperty()
	SPA_DRT= db.StringProperty()
	SPA_DWF= db.StringProperty()
	SPA_EABOR= db.StringProperty()
	SPA_EW= db.StringProperty()
	SPA_FA= db.StringProperty()
	SPA_FDP= db.StringProperty()
	SPA_FINDIF= db.StringProperty()
	SPA_FRU= db.StringProperty()
	SPA_GF= db.StringProperty()
	SPA_HSC= db.StringProperty()
	SPA_HV= db.StringProperty()
	SPA_I= db.StringProperty()
	SPA_IMPU= db.StringProperty()
	SPA_INT= db.StringProperty()
	SPA_INTI= db.StringProperty()
	SPA_INTP= db.StringProperty()
	SPA_IRR= db.StringProperty()
	SPA_LE= db.StringProperty()
	SPA_LF= db.StringProperty()
	SPA_LI= db.StringProperty()
	SPA_LM= db.StringProperty()
	SPA_MARC= db.StringProperty()
	SPA_MEDDIF= db.StringProperty()
	SPA_MEDNC= db.StringProperty()
	SPA_ML= db.StringProperty()
	SPA_MOTREST= db.StringProperty()
	SPA_MS= db.StringProperty()
	SPA_MUT= db.StringProperty()
	SPA_OT= db.StringProperty()
	SPA_PACH= db.StringProperty()
	SPA_PAP= db.StringProperty()
	SPA_PER= db.StringProperty()
	SPA_PHY= db.StringProperty()
	SPA_PS= db.StringProperty()
	SPA_PSC= db.StringProperty()
	SPA_PSEC= db.StringProperty()
	SPA_PSL= db.StringProperty()
	SPA_RECREL= db.StringProperty()
	SPA_RRA= db.StringProperty()
	SPA_S= db.StringProperty()
	SPA_SIDI= db.StringProperty()
	SPA_SM= db.StringProperty()
	SPA_SPP= db.StringProperty()
	SPA_SSTR= db.StringProperty()
	SPA_URGSUSE= db.StringProperty()
	SPA_VHA= db.StringProperty()
	SPA_WPP= db.StringProperty()
	SPA_WSTR= db.StringProperty()
	SPA_other_txt= db.StringProperty()
	TI_CSB= db.StringProperty()
	TI_PSB= db.StringProperty()
	TI_PSCR= db.StringProperty()
	TI_conf_behav= db.StringProperty()
	TI_decis_balnc= db.StringProperty()
	TI_emot_supp= db.StringProperty()
	TI_encour= db.StringProperty()
	TI_explore= db.StringProperty()
	TI_other_txt= db.StringProperty()
	TI_play_therapy= db.StringProperty()
	TI_pos_reinforce= db.StringProperty()
	TI_prob_solv= db.StringProperty()
	TI_real_test= db.StringProperty()
	TI_refl_listen= db.StringProperty()
	TI_valid= db.StringProperty()

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
        i = Insurance()
        i.name = "BlueCrossBlueShield"
        i.mod_code = "90000"
        i.modality_of_session = "Group"
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
        parms['pid'] = str(hs.md5(parms['lname']).hexdigest())
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

    def post(self):
        user = users.get_current_user()
        uid = user.user_id()

        parms = {}
        for (k,v) in self.request.POST.items():
            parms[k] = v
            query = db.Query(Insurance)

        # get insurance code
        query.filter('name =', parms['insurance'])
        query.filter('modality_of_session =', parms['modality'])
        res = list(query.run(limit=1))
        parms['mod_code'] = res[0].mod_code
        parms['is_billed'] = False

        user_date_lst = parms['date'].split('/')
        parms['date_object'] = d(int(user_date_lst[2]), int(user_date_lst[0]), int(user_date_lst[1]))
        parms['timestamp'] = dt.now()
        parms['session_id'] = str(r.randint(0, 10000000000))

        # increment session number for patient
        query = db.Query(Patient)
        query.filter('user_id = ', uid)        
        query.filter('pid =', parms['patient_id'])
        patient = list(query.run(limit=1))[0]
        db.run_in_transaction(patient.increment, 1)
        parms['session_number'] = patient.session_number

        parms['user_id'] = uid
        
        session = Session(**parms)
        session.put()

        self.redirect('/')

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        user = users.get_current_user()
        uid = user.user_id()

        query = db.Query(Session)
        query.order('-date_object')
        query.filter('user_id = ', uid)

        pid = self.request.get('pid')

        if pid !=  "" or pid:
            query.filter('patient_id = ', pid)


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
