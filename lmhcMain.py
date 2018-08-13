import webapp2

import lmhcHandlers as hh

app = webapp2.WSGIApplication([

    ('/', hh.MainPage),
    ('/patient', hh.PatientHandler),
    ('/sessions', hh.SessionsHandler),
    ('/insurance', hh.InsuranceHandler),
    ('/billing', hh.BillingHandler),
    ('/email', hh.EmailHandler),
    ('/insurance_init', hh.Insurance_init),
    ('/test',hh.TestHandler),
    ('/get',hh.GetHandler),

], debug=True)
