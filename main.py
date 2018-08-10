#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib
import urllib2

from google.appengine.api import users

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

# [START main_page]

class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
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
        }

        template = JINJA_ENVIRONMENT.get_template('index2.html')
        self.response.write(template.render(template_values))
# [END main_page]

class AK(webapp2.RequestHandler):

    def get(self):
        parms = {
            'pid': self.request.get('pid'),
        }
        r = urllib2.urlopen("http://arikarchmer.com/sessions?" + urllib.urlencode(parms))
        self.response.write(r.read())

class PP(webapp2.RequestHandler):

    def get(self):
        r = urllib2.urlopen("http://arikarchmer.com/patients")
        self.response.write(r.read())

class NP(webapp2.RequestHandler):

    def post(self):
        parms = {
            'fname': self.request.get('fname'),
            'lname': self.request.get('lname'),
            'dob': self.request.get('dob'),
            'insurance': self.request.get('insurance'),
        }
        url = "/patients?" + urllib.urlencode(parms)
        r = urllib2.urlopen(url)
        #self.redirect(url)
        
class NS(webapp2.RequestHandler):

    def post(self):
        parms = {}
        for (k,v) in self.request.POST.items():
            parms[k] = v

        self.response.write(parms)
        #url = "http://arikarchmer.com/sessions?" + urllib.urlencode(parms)
        #self.redirect(url)

class DU(webapp2.RequestHandler):

    def get(self):
        r = urllib2.urlopen("http://arikarchmer.com/email")
        self.response.write(r.read())


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/ak',AK),
    ('/pp',PP),
    ('/np',NP),
    ('/ns',NS),
    ('/du',DU),
], debug=True)
# [END app]
