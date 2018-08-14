import json
import jinja2
import webapp2
import os
import urllib
import urllib2
import logging
import datetime
import random as r
from google.appengine.api import users
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def ndb_user_key(uid):
    """Constructs a Datastore key for a User entity.
    """
    return ndb.Key('User', uid)

class ModelEncoder(json.JSONEncoder):
    def default(self, obj): 

        if isinstance(obj, ndb.Model): 
            properties = obj._properties.items() 
            output = {'id': obj.key.urlsafe()} 
            for field, value in properties: 
                output[field] = getattr(obj, field)
            return output
        elif isinstance(obj, datetime.datetime):
            return str(obj)
        elif isinstance(obj, datetime.date):
            return "%02i/%02i/%i"%(obj.month,obj.day,obj.year)

        return json.JSONEncoder.default(self, obj) 


class Patient(ndb.Model):

    name = ndb.StringProperty()
    dob = ndb.StringProperty(indexed=False)
    insurance = ndb.StringProperty()
    session_number = ndb.IntegerProperty(indexed=False)

    def increment(self, amount=1):
        self.session_number += amount
        self.put()


class Session(ndb.Model):

    patient_id = ndb.StringProperty()

    is_billed = ndb.BooleanProperty()
    billing_time = ndb.DateTimeProperty()
    insurance = ndb.StringProperty()
    mod_code = ndb.StringProperty(indexed=False)

    session_number = ndb.IntegerProperty(indexed=False)

    date = ndb.StringProperty(indexed=False)
    date_object = ndb.DateProperty()
    timestamp = ndb.DateTimeProperty()

    name = ndb.StringProperty()

    dob = ndb.StringProperty(indexed=False)
    diag = ndb.StringProperty(indexed=False)
    diag_code = ndb.StringProperty()
    modality = ndb.StringProperty()
    new_issue = ndb.StringProperty(indexed=False)
    no_new_issue = ndb.StringProperty(indexed=False)

    ASS_ABLE= ndb.StringProperty(indexed=False)
    ASS_CONST= ndb.StringProperty(indexed=False)
    ASS_COOP= ndb.StringProperty(indexed=False)
    ASS_EFFRT= ndb.StringProperty(indexed=False)
    ASS_INSIG= ndb.StringProperty(indexed=False)
    ASS_OR= ndb.StringProperty(indexed=False)
    ASS_other_txt= ndb.StringProperty(indexed=False)
    ASS_present= ndb.StringProperty(indexed=False)
    ASS_present_txt= ndb.StringProperty(indexed=False)
    G_1_decr= ndb.StringProperty(indexed=False)
    G_1_decr_txt= ndb.StringProperty(indexed=False)
    G_1_impr= ndb.StringProperty(indexed=False)
    G_1_impr_txt= ndb.StringProperty(indexed=False)
    G_2_decr= ndb.StringProperty(indexed=False)
    G_2_decr_txt= ndb.StringProperty(indexed=False)
    G_2_impr= ndb.StringProperty(indexed=False)
    G_2_impr_txt= ndb.StringProperty(indexed=False)
    G_cop_skills= ndb.StringProperty(indexed=False)
    G_expr= ndb.StringProperty(indexed=False)
    G_id_res= ndb.StringProperty(indexed=False)
    G_other_txt= ndb.StringProperty(indexed=False)
    G_sc_skills= ndb.StringProperty(indexed=False)
    G_verb= ndb.StringProperty(indexed=False)
    PLN_CONT= ndb.StringProperty(indexed=False)
    PLN_FREQ= ndb.StringProperty(indexed=False)
    PLN_NXT= ndb.StringProperty(indexed=False)
    PLN_PSY= ndb.StringProperty(indexed=False)
    PLN_other_txt= ndb.StringProperty(indexed=False)
    RA_none= ndb.StringProperty(indexed=False)
    RA_others_att= ndb.StringProperty(indexed=False)
    RA_others_idea= ndb.StringProperty(indexed=False)
    RA_others_plan= ndb.StringProperty(indexed=False)
    RA_prop_att= ndb.StringProperty(indexed=False)
    RA_prop_idea= ndb.StringProperty(indexed=False)
    RA_prop_plan= ndb.StringProperty(indexed=False)
    RA_self_att= ndb.StringProperty(indexed=False)
    RA_self_idea= ndb.StringProperty(indexed=False)
    RA_self_plan= ndb.StringProperty(indexed=False)
    SPA_ACTOUT= ndb.StringProperty(indexed=False)
    SPA_AGI= ndb.StringProperty(indexed=False)
    SPA_AHA= ndb.StringProperty(indexed=False)
    SPA_ALCHUSE= ndb.StringProperty(indexed=False)
    SPA_ANG= ndb.StringProperty(indexed=False)
    SPA_ARG= ndb.StringProperty(indexed=False)
    SPA_AX= ndb.StringProperty(indexed=False)
    SPA_DIFTRAN= ndb.StringProperty(indexed=False)
    SPA_DIT= ndb.StringProperty(indexed=False)
    SPA_DM= ndb.StringProperty(indexed=False)
    SPA_DRGUSE= ndb.StringProperty(indexed=False)
    SPA_DRT= ndb.StringProperty(indexed=False)
    SPA_DWF= ndb.StringProperty(indexed=False)
    SPA_EABOR= ndb.StringProperty(indexed=False)
    SPA_EW= ndb.StringProperty(indexed=False)
    SPA_FA= ndb.StringProperty(indexed=False)
    SPA_FDP= ndb.StringProperty(indexed=False)
    SPA_FINDIF= ndb.StringProperty(indexed=False)
    SPA_FRU= ndb.StringProperty(indexed=False)
    SPA_GF= ndb.StringProperty(indexed=False)
    SPA_HSC= ndb.StringProperty(indexed=False)
    SPA_HV= ndb.StringProperty(indexed=False)
    SPA_I= ndb.StringProperty(indexed=False)
    SPA_IMPU= ndb.StringProperty(indexed=False)
    SPA_INT= ndb.StringProperty(indexed=False)
    SPA_INTI= ndb.StringProperty(indexed=False)
    SPA_INTP= ndb.StringProperty(indexed=False)
    SPA_IRR= ndb.StringProperty(indexed=False)
    SPA_LE= ndb.StringProperty(indexed=False)
    SPA_LF= ndb.StringProperty(indexed=False)
    SPA_LI= ndb.StringProperty(indexed=False)
    SPA_LM= ndb.StringProperty(indexed=False)
    SPA_MARC= ndb.StringProperty(indexed=False)
    SPA_MEDDIF= ndb.StringProperty(indexed=False)
    SPA_MEDNC= ndb.StringProperty(indexed=False)
    SPA_ML= ndb.StringProperty(indexed=False)
    SPA_MOTREST= ndb.StringProperty(indexed=False)
    SPA_MS= ndb.StringProperty(indexed=False)
    SPA_MUT= ndb.StringProperty(indexed=False)
    SPA_OT= ndb.StringProperty(indexed=False)
    SPA_PACH= ndb.StringProperty(indexed=False)
    SPA_PAP= ndb.StringProperty(indexed=False)
    SPA_PER= ndb.StringProperty(indexed=False)
    SPA_PHY= ndb.StringProperty(indexed=False)
    SPA_PS= ndb.StringProperty(indexed=False)
    SPA_PSC= ndb.StringProperty(indexed=False)
    SPA_PSEC= ndb.StringProperty(indexed=False)
    SPA_PSL= ndb.StringProperty(indexed=False)
    SPA_RECREL= ndb.StringProperty(indexed=False)
    SPA_RRA= ndb.StringProperty(indexed=False)
    SPA_S= ndb.StringProperty(indexed=False)
    SPA_SIDI= ndb.StringProperty(indexed=False)
    SPA_SM= ndb.StringProperty(indexed=False)
    SPA_SPP= ndb.StringProperty(indexed=False)
    SPA_SSTR= ndb.StringProperty(indexed=False)
    SPA_URGSUSE= ndb.StringProperty(indexed=False)
    SPA_VHA= ndb.StringProperty(indexed=False)
    SPA_WPP= ndb.StringProperty(indexed=False)
    SPA_WSTR= ndb.StringProperty(indexed=False)
    SPA_other_txt= ndb.StringProperty(indexed=False)
    TI_CSB= ndb.StringProperty(indexed=False)
    TI_PSB= ndb.StringProperty(indexed=False)
    TI_PSCR= ndb.StringProperty(indexed=False)
    TI_conf_behav= ndb.StringProperty(indexed=False)
    TI_decis_balnc= ndb.StringProperty(indexed=False)
    TI_emot_supp= ndb.StringProperty(indexed=False)
    TI_encour= ndb.StringProperty(indexed=False)
    TI_explore= ndb.StringProperty(indexed=False)
    TI_other_txt= ndb.StringProperty(indexed=False)
    TI_play_therapy= ndb.StringProperty(indexed=False)
    TI_pos_reinforce= ndb.StringProperty(indexed=False)
    TI_prob_solv= ndb.StringProperty(indexed=False)
    TI_real_test= ndb.StringProperty(indexed=False)
    TI_refl_listen= ndb.StringProperty(indexed=False)
    TI_valid= ndb.StringProperty(indexed=False)

    notes = ndb.TextProperty()


class Insurance(ndb.Model):

    name = ndb.StringProperty()
    mod_code = ndb.StringProperty()
    modality_of_session = ndb.StringProperty()


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

        
class PatientHandler(webapp2.RequestHandler):

    def post(self):
        user = users.get_current_user()

        parms = {}
        for (k,v) in self.request.POST.items():
            parms[k] = v
        parms['session_number'] = int(parms['session_number'] or "0")
        parms['parent'] = ndb_user_key(user.user_id())
        p = Patient(**parms)
        p.put()

        self.redirect('/')

    def get(self):

        user = users.get_current_user()
        uid = user.user_id()

        query = Patient.query(ancestor=ndb_user_key(uid))

        s = list(query.fetch())
        obj = {'patient_list': s}

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(obj, cls=ModelEncoder))



class BillingHandler(webapp2.RequestHandler):

    def get(self):

    	user = users.get_current_user()
        uid = user.user_id()

        query = Session.query(ancestor=ndb_user_key(uid))
        query = query.filter(Session.is_billed == False)
        query = query.order(Session.name)

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

        query = Insurance.query()
        query = query.filter(Insurance.name == parms['insurance'])
        query = query.filter(Insurance.modality_of_session == parms['modality'])
        res = list(query.fetch(limit=1))

        parms['mod_code'] = res[0].mod_code
        parms['is_billed'] = False

        user_date_lst = parms['date'].split('/')
        parms['date_object'] = datetime.date(int(user_date_lst[2]), int(user_date_lst[0]), int(user_date_lst[1]))
        parms['timestamp'] = datetime.datetime.now()

        # increment number of sessions for patient
        key = ndb.Key(urlsafe=parms['patient_id'])
        patient = key.get()
        ndb.transaction(patient.increment)
        parms['session_number'] = patient.session_number

        parms['parent'] = ndb_user_key(user.user_id())

        del parms['seshNo']
        del parms['session_id']
        
        session = Session(**parms)
        session.put()

        self.redirect('/')

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        user = users.get_current_user()
        uid = user.user_id()

        query = Session.query(ancestor=ndb_user_key(uid))

        query = query.order(-Session.date_object)

        pid = self.request.get('pid')

        if pid !=  "" or pid:
            query = query.filter(Session.patient_id == pid)

        obj = list(query.fetch(limit=200))

        self.response.write(json.dumps(obj, cls=ModelEncoder))
