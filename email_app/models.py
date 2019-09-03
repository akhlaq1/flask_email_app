from email_app import db

class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(300), unique=True, nullable=False)
    subject = db.Column(db.String(300), unique=False, nullable=False)
    message  = db.Column(db.String(300), unique=False, nullable=True)
    dt  = db.Column(db.Date, unique=False, nullable=False)
    send_num = db.Column(db.Integer, unique=False, nullable=False, default = 0)
    follow_up = db.Column(db.Integer, unique=False, nullable=False, default = 0)
    last_contacted = db.Column(db.Date, unique=False, nullable=True)

def __repr__(self):
        return f'''Emails('{self.email}','{self.subject}','{self.message}','{self.dt}','{self.send_num}','{self.follow_up}','{self.last_contacted}')
'''
