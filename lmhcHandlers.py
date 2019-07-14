import json
import jinja2
import webapp2
import os
import datetime
import hashlib as hs
import time
import re
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images


import models
import sessions


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):


    def get(self):
        user = users.get_current_user()

        permitted = models.EmailHash.validate(user.email())
        waiver = models.EmailHash.has_waiver(user.email())

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
            'permission': permitted and waiver,
            'waiver': permitted and not waiver,
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
        hash.email = email
        hash.waiver = True
        hash.put()

        self.redirect('/')


class Permissions_init(webapp2.RequestHandler):

    def get(self):

        email = self.request.get('email', None)
        if email:
            ident = hs.md5(email).hexdigest()
            eh = models.EmailHash(id = ident)
            eh.Hash = ident
            eh.waiver = False
            eh.email = email
            #eh.name = "Mauricio Karchmer, LMHC"
            eh.put()
            self.response.write(email + " registered")
            return
        else:
            self.response.write("nothing to do")

        # if False:
        #     ident = '361e54ab7e96f7610187da7ba3691184'
        #     eh = models.EmailHash(id = ident)
        #     eh.Hash = ident
        #     eh.put()
        #     ident = 'bdb63475a053e834d0fd1a1d93d5034e'
        #     eh = models.EmailHash(id = ident)
        #     eh.Hash = ident
        #     eh.put()
        #     ident = '6215d7ccc7413110ea60829fb1284565'
        #     eh = models.EmailHash(id = ident)
        #     eh.Hash = ident
        #     eh.put()
        #     ident = 'd980f0ec1b5d23bd04ed702536e4b90f'
        #     eh = models.EmailHash(id = ident)
        #     eh.Hash = ident
        #     eh.put()
        #     self.response.write("done!")
        #     return


class Insurance_init(webapp2.RequestHandler):

    def get(self):

        for carrier in ['BlueCrossBlueShield', 'Tufts', 'HarvardPilgrim', 'Optum', 'Cypress', 'Cigna']:
        #for carrier in ['Cigna']:
        
            i = models.Insurance()
            i.name = carrier
            i.mod_code = "90846"
            i.modality_of_session = "Family without patient"
            i.put()
            if False:
                # for backward compatibility
                i = models.Insurance()
                i.name = carrier
                i.mod_code = "90834"
                i.modality_of_session = "Individual"
                i.put()
            i = models.Insurance()
            i.name = carrier
            i.mod_code = "90834"
            i.modality_of_session = "Individual-45min"
            i.put()
            i = models.Insurance()
            i.name = carrier
            i.mod_code = "90832"
            i.modality_of_session = "Individual-30min"
            i.put()
            i = models.Insurance()
            i.name = carrier
            i.mod_code = "90837"
            i.modality_of_session = "Individual-60min"
            i.put()
            if True:
                i = models.Insurance()
                i.name = carrier
                i.mod_code = "90847"
                i.modality_of_session = "Family with patient"
                i.put()
                i = models.Insurance()
                i.name = carrier
                i.mod_code = "90853"
                i.modality_of_session = "Group"
                i.put()
                i = models.Insurance()
                i.name = carrier
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

        patient_id = parms.get('patient_id')
        del parms['patient_id']
        parms['session_number'] = int(parms['session_number'] or "0")

        if patient_id is None or patient_id == "":
            parms['parent'] = models.UserKey.get(user.user_id())
            p = models.Patient(**parms)
            p.put()
        else:
            key = ndb.Key(urlsafe=patient_id)
            p = key.get()
            for k,v in parms.items():
                setattr(p, k, v)
                p.put()

        self.redirect('/')

    def get(self):

        user = users.get_current_user()
        uid = user.user_id()

        query = models.Patient.query(ancestor=models.UserKey.get(uid))

        s = list(query.fetch())
        obj = {'patient_list': s}

        self.response.headers['Content-Type'] = 'application/json;charset=UTF-8'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'DELETE, HEAD, GET, OPTIONS, POST, PUT'
        self.response.headers['Access-Control-Max-Age'] = '1728000'
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

        self.response.headers['Content-Type'] = 'application/json;charset=UTF-8'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'DELETE, HEAD, GET, OPTIONS, POST, PUT'
        self.response.headers['Access-Control-Max-Age'] = '1728000'
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

        img = self.request.get('img-file')

        parms = {}
        for (k,v) in self.request.POST.items():
            parms[k] = v

        session_id = parms.get('session_id', None)

        del parms['session_id']
        del parms['seshNo']

        new_image = None

        if 'notes-attached' in parms and parms['notes-attached'] == 'on' and img:
            k = models.NoteImage.create(parms, img)
            parms['notes_img_id'] = k
            parms['notes'] = '<img class="img-responsive" src="/img?img_id=%s"></img>' % k
            new_image = k
        #else:
        #    parms['notes_img_id'] = None

        if 'notes-attached' in parms:
            del parms['notes-attached']
        if 'img-file' in parms:
            del parms['img-file']

        if 'to-do' in parms:
            del parms['to-do']

        if parms['modality'] == 'Other':
            if parms['mod_code'] == '':
                parms['mod_code'] = 'Invalid'
        else:
            if parms['insurance'] != 'None' and parms['insurance'] != 'SelfPay':
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
            if (session.notes_img_id and new_image):
                n_key = ndb.Key(urlsafe=session.notes_img_id)
                n_key.delete()
            

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
                setattr(session, k, v)

            if (not session.notes.startswith('<img')) and (session.notes_img_id != "") and (session.notes_img_id):

                n_key = ndb.Key(urlsafe=session.notes_img_id)
                n_key.delete()
                session.notes_img_id = None

            session.put()

        self.redirect('/')

    def get(self):

        user = users.get_current_user()
        uid = user.user_id()

        query = models.Session.query(ancestor=models.UserKey.get(uid))

        order = self.request.get('order', 'lifo')
        if order == 'lifo':
            query = query.order(-models.Session.date_object)
        else:
            query = query.order(models.Session.date_object)

        pid = self.request.get('pid')

        if pid !=  "" or pid:
            query = query.filter(models.Session.patient_id == pid)

        limit = int(self.request.get('limit', '600'))
        obj = list(query.fetch(limit=limit))

        if order == 'fifo':
            obj.sort(key=lambda x: x.date_object, reverse=False)


        self.response.headers['Content-Type'] = 'application/json;charset=UTF-8'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'DELETE, HEAD, GET, OPTIONS, POST, PUT'
        self.response.headers['Access-Control-Max-Age'] = '1728000'
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

        self.response.headers['Content-Type'] = 'application/json;charset=UTF-8'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'DELETE, HEAD, GET, OPTIONS, POST, PUT'
        self.response.headers['Access-Control-Max-Age'] = '1728000'
        self.response.write(json.dumps(obj, cls=models.ModelEncoder))

         
class PrintHandler(webapp2.RequestHandler):

    def get(self):

        import formCreator as fc

        user = users.get_current_user()
        uid = user.user_id()
        generator = fc.FormGenerator(models.EmailHash.get_name(user.email()))

        sid = self.request.get('sid')
        if sid != '':
            key = ndb.Key(urlsafe=sid)
            session = key.get()
            pdfFile = generator.getPDF(session)
        else:
            pid = self.request.get('pid')
            name = self.request.get('name')
            start_date = self.request.get('start')
            end_date = self.request.get('end')

            start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y').date()
            end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y').date()

            query = models.Session.query(ancestor=models.UserKey.get(uid))
            query = query.filter(models.Session.patient_id==pid)
            query = query.order(models.Session.date_object)
            obj = [r for r in query.fetch(limit=200)]
            #print "length= ", len(obj)

            merger = fc.FormMerger()
            for s in obj:
                #print s.date, s.date_object
                if start_date <= s.date_object <= end_date:
                    #print "generating"
                    p = generator.getPDF(s)
                    merger.addPdf(p)
                #break

            pdfFile = merger.getPdf()


        #pdfFile = fc.FormGenerator.emptyPDF()

        self.response.headers['content-type'] = 'application/pdf'
        self.response.headers['Content-Disposition'] = 'attachment; filename=form.pdf'
        self.response.out.write(pdfFile.getvalue())


class DeleteHandler(webapp2.RequestHandler):

    def post(self):
        user = users.get_current_user()
        uid = user.user_id()

        parms = {}
        for (k,v) in self.request.POST.items():
            parms[k] = v

        sid = parms.get('sid',None)

        if sid is None:
            self.response.write(json.dumps({
                'status':'error',
                'message':'Nothing to delete.'}))
            return

        s_key = ndb.Key(urlsafe=sid)
        session = s_key.get()

        pid = getattr(session, 'patient_id')

        p_key = ndb.Key(urlsafe=pid)
        patient = p_key.get()

        notes_img_id = getattr(session, 'notes_img_id')
        if notes_img_id is not None and notes_img_id != "":
            n_key = ndb.Key(urlsafe=notes_img_id)
            n_key.delete()  

        # is it OK to delete?
        if patient.session_number > session.session_number:
            self.response.write(json.dumps({
                'status':'error',
                'message':'Attempting to delete a session previous to last. Nothing done.'}))
            return
        if session.is_billed:
            self.response.write(json.dumps({
                'status':'error',
                'message':'Attempting to delete a billed session. Nothing done.'}))
            return

        s_key.delete()
        ndb.transaction(patient.decrement)

        self.response.write(json.dumps({
            'status':'success',
            'message': 'Session deleted',
            'patient': patient.to_dict(),
            'session': session.to_dict()}, cls=models.ModelEncoder))
        return


class NewHandler2(webapp2.RequestHandler):

    def post(self):
        for (k,v) in self.request.POST.items():
            pass
            #print k, v

        img = self.request.get('img-file-todo')
        if img and img!="":
            k = models.NoteImage.create({'name':'mk','date':'today'}, img)
            self.response.write('<img class="img-responsive" src="/img?img_id=%s"></img>' % k) 
            return

        self.response.write(json.dumps({
                    'status':'error',
                    'message':'ERROR'}))


class NewHandler(webapp2.RequestHandler):

    def post(self):

        user = users.get_current_user()
        uid = user.user_id()

        self.response.headers['Content-Type'] = 'application/json'

        parms = {}
        for (k,v) in self.request.POST.items():
            parms[k] = v

        date = parms.get('date',None)
        pid = parms.get('pid',None)
        sid = parms.get('sid',None)
        notes = parms.get('notes-todo', 'TODO')
        img = self.request.get('img-file-todo')

        # update TODO session
        if sid is not None:
            if notes == 'TODO' and img == "":
                self.response.write(json.dumps({
                    'status':'error',
                    'message':'Nothing to change.'}))
                return

            key = ndb.Key(urlsafe=sid)
            session = key.get()

            if session.notes != "TODO":
                self.response.write(json.dumps({
                    'status':'error',
                    'message':'ERROR: trying to change notes of finished session'}))
                return

            if img and img != "":
                k = models.NoteImage.create({'name':session.name,'date':session.date}, img)
                session.notes_img_id = k
                session.notes = '<img class="img-responsive" src="/img?img_id=%s"></img>' % k
            else:
                session.notes = "Client reported: " + notes

            session.put()

            self.response.write(json.dumps({
                'status':'ok',
                'new_session':session.to_dict(),
                }, cls=models.ModelEncoder))
            return


        if date is None or pid is None:
            self.response.write(json.dumps({
                'status':'error',
                'message':'missing arguments'}))
            return

        latest = sessions.find_latest(uid, pid)
        if latest is None:
            self.response.write(json.dumps({
                'status':'error',
                'message':'Cannot use for first session'}))
            return

        date_object = datetime.datetime.strptime(date, '%m/%d/%Y').date()
        latest_date_object = datetime.datetime.strptime(latest.date, '%m/%d/%Y').date()

        if date_object <= latest_date_object:
            self.response.write(json.dumps({
                'status':'error',
                'message':'Latest session is dated %s which is on or after %s'%(latest.date, date)}))
            return

        key = ndb.Key(urlsafe=pid)
        patient = key.get()

        new_session = sessions.new_session(uid, patient, latest, date)

        if new_session is None:
            self.response.write(json.dumps({
                'status':'error',
                'message':'Unknown error creating new session'}))
            return

        new_session.notes = notes
        new_session.put()

        self.response.write(json.dumps({
            'status':'ok',
            'new_session': new_session,
            'latest':latest.to_dict(),
            }, cls=models.ModelEncoder))


class ImageHandler(webapp2.RequestHandler):

    def get(self):
        key = ndb.Key(urlsafe=self.request.get('img_id'))
        img = key.get()
        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(img.blob)
