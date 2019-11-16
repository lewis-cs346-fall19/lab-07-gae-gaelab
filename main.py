import webapp2, MySQLdb, passwords
from random import getrandbits

class MainPage(webapp2.RequestHandler):
    
    def get(self):

        increment = "<p><form action='/' method='post'><input type=hidden value=1><input type='submit' value='Increment'/></form>"
        
        self.response.headers["Content-Type"] = "text/html"

        cookie = self.request.cookies.get("csc346gae")

        if cookie:   
            conn = MySQLdb.connect(unix_socket = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD,db = 'lab7')
            cursor = conn.cursor()
            cursor.execute("SELECT user_name, value FROM sessions WHERE session_id=%s;",(cookie,))
            results = cursor.fetchall()
            user_name = results[0][0]
            value = int(results[0][1])
            self.response.write("Hello " + user_name) 
            self.response.write("Your current value is " + str(value) + ". Press the increment button to increase it by one!")  
            self.response.write(increment) 
                
        else:

            create_user_name = "<p> Welcome, please create a user name to continue<br><form method='post'>Create User Name: <input type='text' name='user_name'><input type='submit' value='Create'/></form>"

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

            cursor.execute("INSERT INTO sessions (session_id, user_name) VALUES (%s, %s);", (new_session_id, user_name))
            conn.commit()
            conn.close()
            self.redirect("/")


app = webapp2.WSGIApplication([("/", MainPage),], debug=True)
