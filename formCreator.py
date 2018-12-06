import os
from cStringIO import StringIO
import json
import re
import PyPDF2 as pp2

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm

import models

path = os.path.join(os.path.split(__file__)[0], 'static/check.jpg')
CHECK_ON = "<img src='%s' height='3mm' width='3mm'/>"%path
path = os.path.join(os.path.split(__file__)[0], 'static/box.jpg')
CHECK_OFF = '<img src="%s" height="3mm" width="3mm" valign="bottom"/>'%path

GRID = ('GRID',(0,0),(-1,-1),0.3*mm,colors.grey)
BOX = ('BOX',(0,0),(-1,-1),0.3*mm,colors.grey)
MID = ('VALIGN',(0,0),(-1,-1),"MIDDLE")

form = {}
with open('static/form.json') as json_data:
    form = json.load(json_data)
TICheckArr = form['TICheckArr']
GoalsCheckArr = form['GoalsCheckArr']
SPACheckArr = form['SPACheckArr']

def qCheck(q):
	return CHECK_ON if q=="on" else CHECK_OFF
def pCheck(p):
	return CHECK_ON if p else CHECK_OFF

def anti_vowel(s):
    result = re.sub(r'[AEIOU]', '', s[3:], flags=re.IGNORECASE)
    return s[:3]+result
def abbr(p):
	if len(p) < 15:
		return p
	l = p.split(' ')
	p_new = ' '.join([(x if len(x) < 6 else anti_vowel(x)) for x in l])
	return p_new[:15]

def na_q(s):
	if s == "na":
		return "N/A"
	return s


class FormGenerator:

	def __init__(self, provider):
		self.provider = provider

	@classmethod
	def emptyPDF(cls):
		pdfFile = StringIO()
		doc = SimpleDocTemplate(pdfFile,
			pagesize=letter,
			rightMargin=72,leftMargin=72,
			topMargin=36,bottomMargin=18)
		Story=[]
		doc.build(Story)

		return pdfFile

	def getPDF(self, session):

		s = session

		pdfFile = StringIO()

		styles=getSampleStyleSheet() 
		styles.add(ParagraphStyle(name='Left', 
		                        alignment=TA_LEFT,
		                        fontSize=10))
		styles.add(ParagraphStyle(name='LeftSm', 
		                        alignment=TA_LEFT,
		                        fontSize=9))
		styles.add(ParagraphStyle(name='LeftXs', 
		                        alignment=TA_LEFT,
		                        fontSize=8))

		doc = SimpleDocTemplate(pdfFile,
		                        pagesize=letter,
		                        rightMargin=72,leftMargin=72,
		                        topMargin=36,bottomMargin=18)

		Story=[]

		pName = Paragraph("<b>Client: </b> %s" % s.name, styles['LeftSm'])
		pDOB = Paragraph("<b>DoB: </b> %s" % s.dob, styles['LeftSm'])
		pDiagCode = Paragraph("<b>Primary Dx code: </b> %s" % s.diag_code, styles['LeftSm'])
		pDiag = Paragraph("<b>Primary Dx: </b> %s" % s.diag, styles['LeftSm'])
		pMod = Paragraph("<b>Modality: </b> %s" % s.modality, styles['LeftSm'])
		pSes = Paragraph("<b>Session No: </b> %s" % s.session_number, styles['LeftSm'])
		pDate = Paragraph("<b>Date of service: </b> %s" % s.date, styles['LeftSm'])
		row = [[pName, pDOB]]
		row.append([pDiag, pDiagCode])
		if s.diag_2_code is not None and s.diag_2_code != "":
			sDiagCode = Paragraph("<b>Secondary Dx code: </b> %s" % s.diag_2_code, styles['LeftSm'])
			sDiag = Paragraph("<b>Secondary Dx: </b> %s" % s.diag_2, styles['LeftSm'])
			row.append([sDiag, sDiagCode])
		Story.append(Table(row, rowHeights=[4.3*mm]*len(row), style=[BOX, MID]))
		Story.append(Spacer(1, 3))

		# new issue
		pIssue = "<b>New Issue: </b>"
		if s.no_new_issue == "on":
			pIssue += "None reported"
		else:
			pIssue += s.new_issue
		pIssue = Paragraph(pIssue, styles['LeftSm'])
		Story.append(Table([[pMod, pSes, pDate],[pIssue]], rowHeights=[4.3*mm]*2, style=[BOX, MID,('SPAN',(0,-1),(-1,-1))]))

		p = "<b>Risk Assessment: </b>"
		if s.RA_none == "on":
			p += "Danger to None"
		p = Paragraph(p, styles['LeftSm'])
		row = [[p]]
		if s.RA_none != "on":
			Story.append(Spacer(1, 2))
			slfH = "<b>Self </b>"
			slf = "%s Ideation "%(qCheck(s.RA_self_idea))
			slf += "%s Plan "%(qCheck(s.RA_self_plan))
			slf += "%s Attempt "%(qCheck(s.RA_self_att))

			othH = "<b>Others </b>"
			oth = "%s Ideation "%(qCheck(s.RA_others_idea))
			oth += "%s Plan "%(qCheck(s.RA_others_plan))
			oth += "%s Attempt "%(qCheck(s.RA_others_att))

			prpH = "<b>Property </b>"
			prp = "%s Ideation "%(qCheck(s.RA_prop_idea))
			prp += "%s Plan "%(qCheck(s.RA_prop_plan))
			prp += "%s Attempt "%(qCheck(s.RA_prop_att))

			row.append([Paragraph(slfH,styles['LeftSm']),Paragraph(othH,styles['LeftSm']),Paragraph(prpH,styles['LeftSm'])])
			row.append([Paragraph(slf,styles['LeftSm']),Paragraph(oth,styles['LeftSm']),Paragraph(prp,styles['LeftSm'])])
			Story.append(Table(row, spaceBefore=1*mm, rowHeights=[4.3*mm]*len(row), style=[BOX, MID]))
		#Story.append(Spacer(1, 5))

		p = Paragraph("<b>Therapeutic Interventions: </b>", styles['Left'])
		row = [[p]]
		Story.append(Table(row))

		ps = [Paragraph('%s %s'%(qCheck(getattr(s,e[0])),e[1][:28]), styles['LeftXs']) for e in TICheckArr]
		other = Paragraph(' %s Other: %s'%(pCheck(s.TI_other_txt != ""), s.TI_other_txt), styles['LeftXs'])
		ps.append(other)
		ti = map(list, zip(*[iter(ps)]*3))
		Story.append(Table(ti, rowHeights=[4.3*mm]*len(ti), style=[BOX, MID]))
		#Story.append(Spacer(1, 5))

		p = Paragraph("<b>Goals: </b>", styles['Left'])
		row = [[p]]
		Story.append(Table(row))
		ps = []
		ps.append(Paragraph('%s improve <i>%s</i>'%(qCheck(s.G_1_impr),s.G_1_impr_txt), styles['LeftXs']))
		ps.append(Paragraph('%s decrease <i>%s</i>'%(qCheck(s.G_1_decr),s.G_1_decr_txt), styles['LeftXs']))
		if (s.G_2_impr == "on" or s.G_2_decr == "on"):
			ps.append(Paragraph('%s improve <i>%s</i>'%(qCheck(s.G_2_impr),s.G_2_impr_txt), styles['LeftXs']))
			ps.append(Paragraph('%s decrease <i>%s</i>'%(qCheck(s.G_2_decr),s.G_2_decr_txt), styles['LeftXs']))
		if (s.G_3_impr == "on" or s.G_3_decr == "on"):
			ps.append(Paragraph('%s improve <i>%s</i>'%(qCheck(s.G_3_impr),s.G_3_impr_txt), styles['LeftXs']))
			ps.append(Paragraph('%s decrease <i>%s</i>'%(qCheck(s.G_3_decr),s.G_3_decr_txt), styles['LeftXs']))
		gs = map(list, zip(*[iter(ps)]*2))
		Story.append(Table(gs, rowHeights=[4.3*mm]*len(gs), style=[MID]))

		ps = [[Paragraph('%s %s'%(qCheck(getattr(s,e[0])),e[1]), styles['LeftXs']) for e in GoalsCheckArr[:2]]]
		Story.append(Table(ps, rowHeights=[4.3*mm]*len(ps), style=[MID]))
		ps = []
		ps = [[Paragraph('%s %s'%(qCheck(getattr(s,e[0])),e[1]), styles['LeftXs'])] for e in GoalsCheckArr[2:]]
		other = Paragraph('%s Other: %s'%(pCheck(s.G_other_txt != ""), s.G_other_txt), styles['LeftXs'])
		if s.G_other_txt == "":
			ps.append([other])
		Story.append(Table(ps, rowHeights=[4.3*mm]*len(ps), style=[MID]))
		if s.G_other_txt != "":
			ps = []
			ps.append([other])
			Story.append(Table(ps, style=[MID]))
		#Story.append(Spacer(1, 5))

		p = Paragraph("<b>Symptoms / Problem Areas: </b>", styles['Left'])
		row = [[p]]
		Story.append(Table(row))
		ps = [Paragraph('%s %s'%(qCheck(getattr(s,e[0])),e[1][:28]), styles['LeftXs']) for e in SPACheckArr]
		other = Paragraph('%s Other: %s'%(pCheck(s.SPA_other_txt != ""), s.SPA_other_txt), styles['LeftXs'])
		ps.append(other)
		spa = map(list, zip(*[iter(ps)]*3))
		Story.append(Table(spa, rowHeights=[4.3*mm]*len(spa), style=[MID]))
		#Story.append(Spacer(1, 5))

		Story.append(Spacer(1, 3))
		row = [[Paragraph(s.notes, styles['LeftSm'])]]
		Story.append(Table(row, style=[BOX,MID]))
		#Story.append(Spacer(1, 5))

		p = Paragraph("<b>Assessment: </b>", styles['Left'])
		row = [[p]]
		row.append([Paragraph("Client <i>%s</i> use session constructively to address problem areas."%na_q(s.ASS_CONST.lower()),
			styles['LeftXs'])])
		row.append([Paragraph("Client <i>%s</i> show insightfulness, <i>%s</i> show effort in addressing problem areas."%(na_q(s.ASS_INSIG.lower()), na_q(s.ASS_EFFRT.lower())),
			styles['LeftXs'])])
		row.append([Paragraph("Client <i>%s</i> oriented times 3."%na_q(s.ASS_OR.lower()), styles['LeftXs'])])
		row.append([Paragraph("Client <i>%s</i> able to talk about stress factors and how to better manage them."%na_q(s.ASS_ABLE.lower()), 
			styles['LeftXs'])])
		row.append([Paragraph("Client <i>%s</i> cooperative with therapist's efforts to assist him/her with problem areas."%na_q(s.ASS_COOP.lower()), 
			styles['LeftXs'])])
		Story.append(Table(row, rowHeights=[4.3*mm]*len(row), style=[MID]))
		if s.ASS_present_txt != "":
			row = [[Paragraph("Client present with: <i>%s</i>"%s.ASS_present_txt, styles['LeftXs'])]]
			Story.append(Table(row, style=[MID]))
		if s.ASS_other_txt != "":
			row = [[Paragraph("Other: <i>%s</i>"%s.ASS_other_txt, styles['LeftXs'])]]
			Story.append(Table(row, style=[MID]))
		#Story.append(Spacer(1, 5))

		plan = """
		<b><font size=10>Plan:</font></b> Continue <i>%s</i> counseling on a <i>%s</i> basis to work 
		through and to develop coping skills and strategies
		to address problem areas.
		%s Continue psychiatric medications as directed by doctor.
		<u>Next session date:</u> %s
		""" % (s.PLN_CONT.lower(), s.PLN_FREQ.lower(), qCheck(s.PLN_PSY), s.PLN_NXT)
		row = [[Paragraph(plan, styles['LeftXs'])]]
		Story.append(Table(row, style=[MID]))

		prov = Paragraph("<b>Provider:</b> %s"%self.provider, styles['LeftXs'])
		signature = Paragraph("<b>Signature:</b>                 ", styles['LeftXs'])
		date = Paragraph("<b>Date:</b>                 ", styles['LeftXs'])
		row = [[prov, signature, date]]
		Story.append(Table(row, style=[MID]))

		doc.build(Story)

		return pdfFile


class FormMerger:

	def __init__(self):
		self.pw = pp2.PdfFileWriter()

	def addPdf(self, pdfFile):
		pr = pp2.PdfFileReader(pdfFile)
		self.pw.appendPagesFromReader(pr)

	def getPdf(self):
		pdfFile = StringIO()
		self.pw.write(pdfFile)
		return pdfFile


