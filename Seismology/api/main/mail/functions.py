from .. import mailsender
from flask import current_app, render_template
from flask_mail import Message
from smtplib import SMTPException


def sendMail(to, subject, template, **kwargs):
    to = ','.join(to)
    print(to)
    msg = Message(subject, sender = current_app.config['FLASKY_MAIL_SENDER'], recipients = [to])
    try:
        msg.body = render_template(template + '.txt', **kwargs)
        # msg.html = render_template(template + '.html', **kwargs)
        result = mailsender.send(msg)
    except SMTPException as error:
        return "Mail deliver failed" + str(error)
    return True
