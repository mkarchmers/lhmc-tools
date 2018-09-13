import datetime

from google.appengine.ext import ndb

import models

FREQ_MAP = {'Weekly': 7, 'Bi-weekly': 14, 'Monthly': 28}

def new_session(uid, patient, session, date):

	new_session = models.Session(parent=models.UserKey.get(uid), **session.to_dict())

	new_session.date = date
	new_session.date_object = datetime.datetime.strptime(date, '%m/%d/%Y').date()

	new_session.timestamp = datetime.datetime.now()

	new_session.is_billed = False
	new_session.billing_time = None

	new_session.notes = "TODO"

	freq = session.PLN_FREQ
	next_date = new_session.date_object + datetime.timedelta(days=FREQ_MAP[freq])
	new_session.PLN_NXT = next_date.strftime('%m/%d/%Y')

	ndb.transaction(patient.increment)
	new_session.session_number = patient.session_number

	return new_session


def find_latest(uid, patient_id):

	query = models.Session.query(ancestor=models.UserKey.get(uid))
	query = query.order(-models.Session.date_object)
	query = query.filter(models.Session.patient_id == patient_id)

	res = list(query.fetch(limit=1))

	if len(res) > 0:
	    return res[0]

	return None


