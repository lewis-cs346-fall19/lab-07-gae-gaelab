import webapp2, MySQLdb, passwords



class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/html"

                conn = MySQLdb.connect(unix_socket = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD,db = 'testTable')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM testTable");
                results = cursor.fetchall()
                cursor.close()
                print(results)
                self.response.write("gahaaahahahahah")

app = webapp2.WSGIApplication([("/", MainPage),], debug=True)
