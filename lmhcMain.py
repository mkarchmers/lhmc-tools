import webapp2

import lmhcHandlers as hh

app = webapp2.WSGIApplication([

    ('/', hh.MainPage),
    ('/patients', hh.PatientHandler),
    ('/sessions', hh.SessionsHandler),
    ('/insurance', hh.InsuranceHandler),
    ('/billing', hh.BillingHandler),
    ('/email', hh.EmailHandler),
    ('/np', hh.NP),
    ('/ns', hh.NS),
    ('/insurance_init', hh.Insurance_init),
    ('/test',hh.TestHandler),
    ('/get',hh.GetHandler),

], debug=True)