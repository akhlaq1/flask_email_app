import re
from flask import render_template, url_for, redirect, request
from email_app.models import Emails
from email_app import db
from email_app import app
from datetime import datetime
import json
from flask import Response

# for email sender
from email.header    import Header
from email.mime.text import MIMEText
from getpass         import getpass
from smtplib         import SMTP_SSL

# apscheduler=2.1.2
from apscheduler.scheduler import Scheduler

cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()

@cron.interval_schedule(hours=0.0155)
def job_function():
    # Do your work here
    def follow_update(num,newid):
        a = dict(
            follow_up = num
        )
        user = Emails.query.filter_by(id=newid).update(a)
        db.session.commit()

    data = Emails.query.all()
    try:
        for item in data:
            if item.last_contacted != None:
                a =item.dt
                b =item.last_contacted
                c = b-a
                diff_date = c.total_seconds() / 86400
                print(diff_date)
                if diff_date >= 10 and diff_date < 30:
                    follow_update(1,item.id)

                elif diff_date >= 30 and diff_date < 60:
                    follow_update(2,item.id)

                elif diff_date >= 60:
                    follow_update(3,item.id)
    except:
        pass


@app.route('/api/send/<id>')
def send_email(id):
    data = Emails.query.get(id)

    login, password = 'akhlaq.computer1@gmail.com', "akhlaq_1010"
    recipients = [login,data.email]

    # create message
    msg = MIMEText(data.message, 'plain', 'utf-8')
    msg['Subject'] = Header(data.subject, 'utf-8')
    msg['From'] = login
    msg['To'] = ", ".join(recipients)

    # send it via gmail
    s = SMTP_SSL('smtp.gmail.com', 465, timeout=20)
    s.set_debuglevel(1)
    try:
        s.login(login, password)
        s.sendmail(msg['From'], recipients, msg.as_string())
        
        a = dict(
            send_num = data.send_num + 1,
            last_contacted = datetime.today(),
            follow_up = False
        )
        user = Emails.query.filter_by(id=id).update(a)
        db.session.commit()

        print("Email sent seuccessfully")
        e = "Email sent seuccessfully"

    except:
        print("Email not sent")
        e ="Email not sent"

    finally:
        s.quit()

    return e

@app.route('/api')
def home_func():
    data = Emails.query.all()
    print(data)
    a = []
    for item in data:
       b =  {
           "id":item.id,
           "email":item.email,
           "subject":item.subject,
           "message":item.message,
           "date":str(item.dt),
           "last_contacted":str(item.last_contacted),
           "send_num":item.send_num,
           "follow_up":item.follow_up
       }
       a.append(b)
    return Response(json.dumps(a),  mimetype='application/json')


@app.route('/api/add', methods=['POST'])
def add():
    try:
        content = request.get_json()
        email1 = Emails(
            email = content['email'],
            subject = content['subject'],
            message = content['message'],
            dt = datetime.today()
    )
        db.session.add(email1)
        db.session.commit()
        e = content
        e = "data added"
    except:
        e = "error in data addition "
        raise
    return e

@app.route('/api/update',methods=['POST'])
def update_func():
    try:
        content = request.get_json()
        a = dict(
                email = content['email'],
                subject = content['subject'],
                message = content['message'],
            )

        user = Emails.query.filter_by(id=content['id']).update(a)
        db.session.commit()
        e = "Data updated"
    except:
        e = "Error in updating, please check logs"
    return e