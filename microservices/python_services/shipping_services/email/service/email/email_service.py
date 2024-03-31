from flask import render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    def __init__(self, mail_server, mail_port, mail_username, mail_password):
        self.mail_server = mail_server
        self.mail_port = mail_port
        self.mail_username = mail_username
        self.mail_password = mail_password

    def send_email(self, subject, sender, recipients, cc=None, **kwargs):
        body = render_template('email_template.html', **kwargs)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        if cc:
            msg['Cc'] = ', '.join(cc)

        part = MIMEText(body, 'html')
        msg.attach(part)

        try:
            server = smtplib.SMTP(self.mail_server, self.mail_port)
            server.starttls()
            server.login(self.mail_username, self.mail_password)
            server.sendmail(sender, recipients + cc if cc else recipients, msg.as_string())
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")
