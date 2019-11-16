import webapp2, MySQLdb, passwords
from random import getrandbits

create_user_name = "<form method='post'>Create User Name: <input type='text' name='user_name'><input type='submit' value='Create'/></form>"

increment = "<form method='post'><input type='submit' value='Increment'/></form>"

class MainPage(webapp2.RequestHandler):
    def get(self):
        
        self.response.headers["Content-Type"] = "text/html"

        cookie = self.request.cookies.get("csc346gae")

        if cookie:   
            conn = MySQLdb.connect(unix_socket = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD,db = 'lab7')
            cursor = conn.cursor()
            cursor.execute("SELECT user_name FROM sessions WHERE session_id=%s;",(cookie,))
            results = cursor.fetchall()
            self.response.write("Hello " + str(results))    

                
        else:
            self.response.write(create_user_name)

        

    def post(self):

        user_name = self.request.get("user_name")
        if user_name == "":
            self.redirect("/")
        else:
            conn = MySQLdb.connect(unix_socket = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD,db = 'lab7')
            cursor = conn.cursor()

            new_session_id = "%032x" % getrandbits(128)
            self.response.set_cookie(key='csc346gae', value=new_session_id, max_age=1800,)

            cursor.execute("INSERT INTO sessions (session_id, user_name) VALUES (%s, %s);", (new_session_id, 'user_name'))
            conn.commit()
            conn.close()
            self.redirect("/")


app = webapp2.WSGIApplication([("/", MainPage),], debug=True)
