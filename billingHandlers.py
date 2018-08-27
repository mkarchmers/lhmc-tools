#

from cStringIO import StringIO
import webapp2
import datetime

from google.appengine.api import users
from google.appengine.api import mail

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

import models

class Test(webapp2.RequestHandler):

    def getData(self):

        user = users.get_current_user()
        uid = user.user_id()

        query = models.Session.query(ancestor=models.UserKey.get(uid))
        query = query.filter(models.Session.is_billed == False)
        query = query.order(models.Session.name)

        sessions = [x for x in query.fetch() if x.insurance != 'None']

        titles = ['Name', 'Session date', 'Procedure code', 'DSM 5', 'Insurance']
        entries = [[s.name, s.date, s.mod_code, s.diag_code, s.insurance] for s in sessions]

        start = None
        end = None

        # find date range
        if len(sessions) > 0:
            first = sessions.pop()
            if first:
                start = datetime.datetime.strptime(first.date,"%m/%d/%Y")
                end = datetime.datetime.strptime(first.date,"%m/%d/%Y")
                for s in sessions:
                    this_start = datetime.datetime.strptime(s.date,"%m/%d/%Y")
                    this_end = datetime.datetime.strptime(s.date,"%m/%d/%Y")
                    if this_start < start:
                        start = this_start
                    if this_end > end:
                        end = this_end

        return {"titles": titles, "entries": entries, "range": (start, end)}

    def mail(self, bill):

        user = users.get_current_user()

        body = '''
            this is my first bill. See attached.
        '''

        mail.send_mail(
            sender= user.email(),
            to= "Mauricio Karchmer <mkarchmers@hotmail.com>",
            subject= "my first bill",
            body= body,
            attachments= [("bill.pdf", bill)],
            )

    def get(self):

        pdfFile = StringIO()

        styles=getSampleStyleSheet() 
        styles.add(ParagraphStyle(name='Right', 
                                alignment=TA_RIGHT,
                                fontSize=11))

        doc = SimpleDocTemplate(pdfFile,
                                pagesize=letter,
                                rightMargin=72,leftMargin=72,
                                topMargin=72,bottomMargin=18)
        Story=[]         
         
        data = self.getData()

        try:
            start, end = (data['range'][0].strftime('%m/%d/%Y'), data['range'][1].strftime('%m/%d/%Y'))
            ptext = 'Sessions from <b>%s</b> to <b>%s</b>' % (start, end)
            Story.append(Paragraph(ptext, styles["Right"]))
            Story.append(Spacer(1, 38))
        except:
            pass

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

        t=Table(matrix, style=tStyle)

        Story.append(t)

        doc.build(Story)

        #self.mail(pdfFile.getvalue())

        self.response.headers['content-type'] = 'application/pdf'
        self.response.headers['Content-Disposition'] = 'attachment; filename=file.pdf'
        self.response.out.write(pdfFile.getvalue())
