#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import cgi
import re

form = """
<form method="post">
    <h1>Signup</h1>
    <br>
    <label> Username <input type="text" name="usern" value="%(usern)s" required><span class="error">%(error_a)s</span></label><br>
    <label> Password <input type="password" name="passw" value="%(passw)s" required><span class="error">%(error_b)s</span></label><br>
    <label> Confirm Password <input type="password" name="verify" value="%(verify)s" required><span class="error">%(error_c)s</span></label><br>
    <label> E-mail <input type="email" name="email" value="%(email)s"><span class="error">%(error_d)s</span></label><br>
    <br>
    <br>
    <input type="submit">
</form>
"""

def valid_username(usern):
    if usern and (' ' not in usern):
        return usern

def valid_password(passw):
    if passw and (' ' not in passw):
        return passw

def verify_password(passw, verify):
    if passw and verify and passw == verify:
        return verify

def valid_email(email):
    if email and ('@' in email):
        return email

def escape_html(s):
    return cgi.escape(s, quote = True)
#t2 = "I think %s and %s are perfectly normal things to do in public"
#def sub2(s1, s2)
#    return t2 % (s1, s2)
#sub2('running', 'sleeping')
#t3 = "I'm %(nickname)s. My real name is %(name)s, but my friends call me %(nickname)s."
#   def sub_m(name, nickname):
#       return t3 % {'name': name, 'nickname': nickname}

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error_a="", error_b="", error_c="", error_d="", usern="", passw="", verify="", email=""):
        self.response.out.write(form % {"error_a": error_a, "error_b": error_b, "error_c": error_c, "error_d": error_d, "usern": escape_html(usern), "passw": escape_html(passw), "verify": escape_html(verify), "email": escape_html(email)})
    def get(self):
        self.write_form()

    def post(self):
        user_username = self.request.get('usern')
        user_password = self.request.get('passw')
        user_email = self.request.get('email')
        user_verify = self.request.get('verify')
        username = valid_username(user_username)
        password = valid_password(user_password)
        verify = verify_password(user_password, user_verify)
        email = valid_email(user_email)

        if not username:
            self.write_form("<font style='color: red'>That is not a valid username!</font>", "", "", "", "", "", "", user_email)
        else:
            if not password:
                self.write_form("", "<font style='color: red'>That is not a valid password!</font>", "", "", user_username, "", "", user_email)
            else:
                if not verify:
                    self.write_form("", "", "<font style='color: red'>Passwords don't match!</font>", "", user_username, "", "", user_email)
                else:
                    if not email:
                        self.write_form("", "", "", "<font style='color: red'>That is not a valid email!</font>", user_username, "", "", "")
                    else:
                        self.redirect("/welcome")

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('usern')
        self.response.write("<h1>Welcome," + username)

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/welcome', WelcomeHandler)
], debug=True)
