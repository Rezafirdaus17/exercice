import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.util import running_sender_email

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b15ce0c676dfde280ba245'
app.config['ASSETS_DEBUG'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

app.config.update(mail_settings)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

scheduler = BackgroundScheduler()
scheduler.configure(timezone="Asia/Singapore")
scheduler.add_job(running_sender_email, trigger="cron", minute="*/1")
scheduler.start()

from app import models, routes
