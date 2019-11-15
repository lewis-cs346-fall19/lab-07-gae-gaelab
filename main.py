import webapp2

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/html"
		self.response.write("Hello world")

app = webapp2.WSGIApplication([("/", MainPage),], debug=True)
