import webapp2

import lmhcHandlers as hh
import billingHandlers as bh

app = webapp2.WSGIApplication([

    ('/', hh.MainPage),
    ('/patient', hh.PatientHandler),
    ('/sessions', hh.SessionsHandler),
    ('/billing', hh.BillingHandler),
    ('/email', hh.EmailHandler),
    ('/schedule', hh.ScheduleHandler),
    ('/insurance_init', hh.Insurance_init),
    ('/permissions_init', hh.Permissions_init),
    ('/bill', bh.BillingHandler2),
    ('/print', hh.PrintHandler),
    ('/new', hh.NewHandler),

], debug=False)
