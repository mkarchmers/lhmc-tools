import webapp2

import lmhcHandlers as hh

app = webapp2.WSGIApplication([

    ('/', hh.MainPage),
    ('/psych', hh.PsychHandler),
    ('/patients', hh.PatientHandler),
    ('/PatientPage', hh.PatientPageHandler),
    ('/addpatient', hh.AddPatientHandler),
    ('/sessions', hh.SessionsHandler),
    ('/SessionList', hh.SessionListHandler),
    ('/SessionFinder', hh.SessionFinderHandler),
    ('/Session', hh.SessionHandler),
    ('/insurance', hh.InsuranceHandler),
    ('/billing', hh.BillingHandler),
    ('/login', hh.LoginPageHandler),
    ('/email', hh.EmailHandler),
    ('/np', hh.NP),
    ('/ns', hh.NS),
    ('/insurance_init', hh.Insurance_init),
    ('/test',hh.TestHandler),
    ('/get',hh.GetHandler),

], debug=True)