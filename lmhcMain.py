import webapp2

import lmhcHandlers as hh

app = webapp2.WSGIApplication([

    ('/', hh.MainPage),
    ('/patient', hh.PatientHandler),
    ('/sessions', hh.SessionsHandler),
    ('/billing', hh.BillingHandler),
    ('/email', hh.EmailHandler),
    ('/insurance_init', hh.Insurance_init),
    ('/permissions_init', hh.Permissions_init)

], debug=True)
