#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Guestbook


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("main.html")

class MessageHandler(BaseHandler):
    def get(self):
        return self.render_template("message.html")

class SendHandler(BaseHandler):
    def post(self):
        firstName = self.request.get("firstName")
        lastName = self.request.get("lastName")
        mail = self.request.get("mail")
        message = self.request.get("message")

        listOfValues = [firstName.lower(),lastName.lower(),mail.lower(),message.lower()]

        if "<script>"  in listOfValues:
            return self.render_template("error.html")
        else:
            guestbook = Guestbook(name=firstName,surname=lastName,email=mail,message=message)
            guestbook.put()

            params = {"firstName":firstName, "lastName":lastName, "mail":mail, "message": message}

            return self.render_template("processed.html",params)

class GuestbookHandler(BaseHandler):
    def get(self):
        infoList = Guestbook.query().fetch()
        params = {"infoList":infoList}

        return self.render_template("guestBook.html",params)

class CheckHandler(BaseHandler):
    def get(self,comment_id):
        comment = Guestbook.get_by_id(int(comment_id))
        params = {"comment":comment}

        return self.render_template("check.html",params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route("/message",MessageHandler),
    webapp2.Route("/send",SendHandler),
    webapp2.Route("/guestbook",GuestbookHandler),
    webapp2.Route("/check/<comment_id:\d+>",CheckHandler)
], debug=True)
