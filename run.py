try:
    import sqlite3

    conn = sqlite3.connect('./email_app/site.db')
    print ("Opened database successfully")

    conn.execute('CREATE TABLE emails(id INTEGER PRIMARY KEY,email TEXT,subject TEXT, message TEXT, dt DATE,last_contacted DATE, send_num INTEGER, follow_up INTEGER )')
    print ("Table created successfully")
    conn.close()
except:
    pass

from email_app import app

from flask_cors import CORS

CORS(app) 

if __name__ == '__main__':
    app.run(debug=True, port=3000)

