import webapp2, MySQLdb, passwords
from random import getrandbits

class MainPage(webapp2.RequestHandler):
    def get(self):
        
        self.response.headers["Content-Type"] = "text/html"
        conn = MySQLdb.connect(unix_socket = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD,db = 'lab7')
        cursor = conn.cursor()
        cookie = self.request.cookies.get("cookie_name")

        if cookie:    
            q = "SELECT user_name FROM sessions;"
                
        else:
            session_id = "%032x" % getrandbits(128)
            self.response.set_cookie('cookie', session_id, max_age=1800)
            cursor.execute("INSERT INTO sessions (session_id, user_name) VALUES (session_id, 'user_name');")
            q = "SELECT user_name FROM sessions;"

        cursor.execute(q);
        results = cursor.fetchall()
        cursor.close()
        self.response.write("Hello " + str(results[1]))    

app = webapp2.WSGIApplication([("/", MainPage),], debug=True)
