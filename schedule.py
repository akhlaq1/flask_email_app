from apscheduler.schedulers.blocking import BlockingScheduler
from email_app.models import Emails
from email_app import db

def scheduler_func():
    data = Emails.query.all()
    for item in data:
        a =item.dt
        b =item.last_contacted
        c = b-a
        diff_date = c.total_seconds() / 86400
        print(diff_date)
        if diff_date >= 10:
            a = dict(
            follow_up = True
        )
            user = Emails.query.filter_by(id=item.id).update(a)
            db.session.commit()

scheduler = BlockingScheduler()
scheduler.add_job(scheduler_func, 'interval', hours=0.0333,max_instances=1)
scheduler.start()