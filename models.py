import json
import datetime
import hashlib as hs
from google.appengine.ext import ndb


class UserKey(object):

	@classmethod
	def get(cls, uid):
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

    name = ndb.StringProperty(indexed=False)
    dob = ndb.StringProperty(indexed=False)
    insurance = ndb.StringProperty(indexed=False)
    session_number = ndb.IntegerProperty(indexed=False)
    status = ndb.StringProperty()

    def increment(self, amount=1):
        self.session_number += amount
        self.put()
    def decrement(self, amount=1):
        self.session_number -= amount
        self.put()


class Session(ndb.Model):

    patient_id = ndb.StringProperty()

    is_billed = ndb.BooleanProperty()
    billing_time = ndb.DateTimeProperty(indexed=False)
    insurance = ndb.StringProperty()
    mod_code = ndb.StringProperty(indexed=False)

    session_number = ndb.IntegerProperty(indexed=False)

    date = ndb.StringProperty(indexed=False)
    date_object = ndb.DateProperty()
    timestamp = ndb.DateTimeProperty(indexed=False)

    name = ndb.StringProperty()

    dob = ndb.StringProperty(indexed=False)
    diag = ndb.StringProperty(indexed=False)
    diag_code = ndb.StringProperty(indexed=False)
    diag_2 = ndb.StringProperty(indexed=False)
    diag_2_code = ndb.StringProperty(indexed=False)
    modality = ndb.StringProperty(indexed=False)
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
    G_3_decr= ndb.StringProperty(indexed=False)
    G_3_decr_txt= ndb.StringProperty(indexed=False)
    G_3_impr= ndb.StringProperty(indexed=False)
    G_3_impr_txt= ndb.StringProperty(indexed=False)
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

    notes = ndb.TextProperty(indexed=False)


class Schedule(ndb.Model):

    name = ndb.StringProperty()
    pid = ndb.StringProperty()
    dow = ndb.StringProperty(indexed=False)
    moment = ndb.StringProperty(indexed=False)
    start = ndb.StringProperty(indexed=False)
    end = ndb.StringProperty(indexed=False)
    freq = ndb.StringProperty(indexed=False)


class EmailHash(ndb.Model):

    Hash = ndb.StringProperty()
    uid = ndb.StringProperty()
    bill = ndb.BooleanProperty()
    pwd = ndb.StringProperty()
    waiver = ndb.BooleanProperty()
    email = ndb.StringProperty()
    name = ndb.StringProperty()

    @classmethod
    def password(cls, email):
        candidate_hash = hs.md5(email.lower()).hexdigest()
        key = ndb.Key(EmailHash, candidate_hash)
        hash = key.get()
        return hash.pwd

    @classmethod
    def billing(cls, email):
        candidate_hash = hs.md5(email.lower()).hexdigest()
        key = ndb.Key(EmailHash, candidate_hash)
        hash = key.get()
        return (hash.bill is not None) and hash.bill

    @classmethod
    def validate(cls, email):
        candidate_hash = hs.md5(email.lower()).hexdigest()
        key = ndb.Key(EmailHash, candidate_hash)
        return key.get() is not None

    @classmethod
    def has_waiver(cls, email):
        candidate_hash = hs.md5(email.lower()).hexdigest()
        key = ndb.Key(EmailHash, candidate_hash)
        hash = key.get()
        return (hash is not None) and (hash.waiver is not None) and hash.waiver

    @classmethod
    def get_name(cls, email):
        candidate_hash = hs.md5(email.lower()).hexdigest()
        key = ndb.Key(EmailHash, candidate_hash)
        hash = key.get()
        return hash.name


class Insurance(ndb.Model):

    name = ndb.StringProperty()
    mod_code = ndb.StringProperty(indexed=False)
    modality_of_session = ndb.StringProperty()

    @classmethod
    def get_code(cls, name, modality):

        query = Insurance.query()
        query = query.filter(Insurance.name == name)
        query = query.filter(Insurance.modality_of_session == modality)
        res = list(query.fetch(limit=1))
        
        return None if len(res) == 0 else res[0].mod_code
