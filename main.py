import webapp2, MySQLdb, passwords
from random import getrandbits

class MainPage(webapp2.RequestHandler):
    def get(self):
        
        self.response.headers["Content-Type"] = "text/html"

        cookie = self.request.cookies.get("cookie_name")

        conn = MySQLdb.connect(unix_socket = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD,db = 'lab7')
        cursor = conn.cursor()

        if cookie:   
            self.response.write(cookie) 
            cursor.execute("SELECT user_name FROM sessions WHERE session_id=%s;",(cookie,))
                
        else:
            self.response.write("<form method='post'>Create User Name: <input type='text' name='user_name'><input type='submit' value='Create'/></form>")
            new_session_id = "%032x" % getrandbits(128)
            self.response.set_cookie(key='cookie_name', value=new_session_id, max_age=1800,)

            cursor.execute("INSERT INTO sessions (session_id, user_name) VALUES (%s, %s);", (new_session_id, 'user_name'))
            conn.commit()
            cursor.execute("SELECT user_name FROM sessions WHERE session_id=%s;",(new_session_id,))

        results = cursor.fetchall()
        self.response.write("Hello " + str(results))    
        conn.close()



app = webapp2.WSGIApplication([("/", MainPage),], debug=True)
