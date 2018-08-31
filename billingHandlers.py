#

from cStringIO import StringIO
import webapp2
import datetime
import pytz

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import ndb

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

import models

class Test(webapp2.RequestHandler):

    def getData(self, end_date, mark):

        def order(a,b):
            nc = cmp(a[0], b[0])
            return cmp(a[1],b[1]) if nc == 0 else nc

        user = users.get_current_user()
        uid = user.user_id()

        query = models.Session.query(ancestor=models.UserKey.get(uid))
        query = query.filter(models.Session.is_billed == False)
        query = query.order(models.Session.name)

        sessions = [x for x in query.fetch() if x.insurance != 'None']

        if end_date is not None:
            sessions = [s for s in sessions if s.date_object <= end_date]

        if mark:
            bill_time = datetime.datetime.now()
            for x in sessions:
                x.billing_time = bill_time
                x.is_billed = True
                x.put()

        titles = ['Name', 'Session date', 'Procedure code', 'DSM 5', 'Insurance']
        entries = [[s.name, s.date, s.mod_code, s.diag_code, s.insurance] for s in sessions]
        entries = sorted(entries, order)

        # find date range
        start = None
        end = None
        if len(sessions) > 0:
            first = sessions.pop()
            if first:
                start = first.date_object
                end = first.date_object
                for s in sessions:
                    if s.date_object < start:
                        start = s.date_object
                    if s.date_object > end:
                        end = s.date_object


        return {"titles": titles, "entries": entries, "range": (start, end)}

    def getPdf(self, user, date, data):

        pdfFile = StringIO()

        styles=getSampleStyleSheet() 
        styles.add(ParagraphStyle(name='Header', 
                                alignment=TA_LEFT,
                                fontSize=13,
                                textColor=colors.red))
        styles.add(ParagraphStyle(name='Right', 
                                alignment=TA_RIGHT,
                                fontSize=11))
        styles.add(ParagraphStyle(name='Left', 
                                alignment=TA_LEFT,
                                fontSize=11))

        doc = SimpleDocTemplate(pdfFile,
                                pagesize=letter,
                                rightMargin=72,leftMargin=72,
                                topMargin=72,bottomMargin=18)
        Story=[]         
         
        Story.append(Paragraph("<i>Westside Billing</i>: Mental Health Billing Service", styles["Header"]))
        Story.append(Spacer(1, 38))

        try:
            start, end = (data['range'][0].strftime('%m/%d/%Y'), data['range'][1].strftime('%m/%d/%Y'))
            ptext = 'Sessions from <b>%s</b> to <b>%s</b>' % (start, end)
            Story.append(Paragraph(ptext, styles["Left"]))
            Story.append(Spacer(1, 38))
        except:
            pass

        Story.append(Paragraph('Provider Name: <b>%s</b>'%user.nickname(), styles["Left"]))
        Story.append(Paragraph(date.strftime('Date: <b>%m/%d/%Y</b>'), 
                                styles['Right']))
        Story.append(Spacer(1, 38))

        P0 = Paragraph('<b>Name:</b>', styles["Normal"])  

        matrix = [ [Paragraph('<b>%s</b>'%t, styles["Normal"]) for t in data['titles']] ]
        matrix.extend(data['entries'])
         
        tStyle = TableStyle([
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND',(0,0),(-1,0),colors.beige), #titles
            ('ALIGN',(2,0),(3,-1),'CENTER'),
            ])

        try:
            # stripe different patients
            c = {1: colors.white, -1: colors.lavenderblush}
            parity = 1
            prevName = data['entries'][0][0]
            for i,e in enumerate(data['entries']):
                if e[0] != prevName:
                    prevName = e[0]
                    parity *= -1
                tStyle.add('BACKGROUND', (0,i+1), (-1,i+1), c[parity])
        except:
            pass

        Story.append(Table(matrix, style=tStyle))

        doc.build(Story)

        return pdfFile

    def mail(self, to, date, body, bill):

        user = users.get_current_user()

        body = '''
            this is my first bill. See attached.
        '''

        mail.send_mail(
            sender= user.email(),
            to= "Mauricio Karchmer <mkarchmers@hotmail.com>",
            subject= "my first bill",
            body= body,
            attachments= [(date.strftime("bill_%m%d%Y.pdf"), bill)],
            )

    def get(self):

        user = users.get_current_user()

        end_date = self.request.get('end', None)
        if end_date is not None:
            end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y').date()

        mark = self.request.get('mark', False)

        date = datetime.datetime.now(pytz.timezone('US/Eastern'))

        data = self.getData(end_date, mark)
        pdfFile = self.getPdf(user, date, data)

        #self.mail(date, None, pdfFile.getvalue())

        self.response.headers['content-type'] = 'application/pdf'
        self.response.headers['Content-Disposition'] = 'attachment; filename=bill_%s.pdf'%date.date()
        self.response.out.write(pdfFile.getvalue())
