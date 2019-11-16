import webapp2, MySQLdb, passwords
from random import getrandbits

class MainPage(webapp2.RequestHandler):
    def get(self):
        
        self.response.headers["Content-Type"] = "text/html"
        conn = MySQLdb.connect(unix_socket = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD,db = 'lab7')
        cursor = conn.cursor()
        cookie = self.request.cookies.get("cookie_name")

        if cookie:   
            self.response.write("I found a cookie") 
            cursor.execute("SELECT user_name FROM sessions WHERE session_id=%s;",(cookie,))
                
        else:
            self.response.write("I did not find a cookie")
            new_session_id = "%032x" % getrandbits(128)
            self.response.set_cookie(key='cookie_name', value=new_session_id, max_age=1800,)
            cursor.execute("INSERT INTO sessions (session_id, user_name) VALUES (%s, %s);", (new_session_id, 'user_name'))
            conn.commit()
            cursor.execute("SELECT user_name FROM sessions WHERE session_id=%s;",(new_session_id,))

        results = cursor.fetchall()
        cursor.close()
        self.response.write("Hello " + str(results[0][0]))    

app = webapp2.WSGIApplication([("/", MainPage),], debug=True)
