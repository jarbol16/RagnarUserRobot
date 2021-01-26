import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
import os
import sys

class Email():
    port = None
    smtp = None
    from_email = None
    pass_email = None
    path = None

    def __init__(self):
        r = os.getcwd()
        self.path = os.getcwd()
        if len(r) > 0:
            self.path = r
        file = open("{0}/config/setting.json".format(self.path))
        print("Constuyendo correo")
        # print (os.path.dirname("{0}/setting.json".format(self.path)))
        # with open('setting.json') as json_data_file:
        data = json.load(file)
        _ = data["email"]
        self.port = _["port"]
        self.smtp = _["smtp"]
        self.from_email = _["from"]
        self.pass_email = _["pass"]

    def send_email(self, to=None, file_name=None, body=None, subject=None):
        print("Correo preprando", file_name)
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = to
        msg['Subject'] = subject
        if file_name:
            print("argv", sys.argv[0])
            attachment = open("{0}/out/{1}".format(self.path, file_name), "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % file_name)
            msg.attach(part)
            try:
                attachment = open("{0}/out/ANS_{1}".format(self.path, file_name), "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % "ANS_"+file_name)
                msg.attach(part)
            except:
                pass
        server = smtplib.SMTP(self.smtp, self.port)
        server.starttls()
        server.login(self.from_email, self.pass_email)
        text = msg.as_string()
        server.sendmail(self.from_email, to, text)
        server.quit()