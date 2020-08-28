import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import logging as log

class Mailing:
    def __init__(self):
        self._enabled = False
        self._myaddr = None
        self._myaddr_pswd = None
        self._toaddr = None

    def setmail(self, myaddr, myaddr_pswd, toaddr):
        self._enabled = True
        self._myaddr = myaddr
        self._myaddr_pswd = myaddr_pswd
        self._toaddr = toaddr
    
    def unsetmail(self):
        self._enabled = False
    
    def sendmail(self, prog):
        subject = "Warning from Taskmaster"
        text = "Your program \'" + prog._name + \
            "\' is down with unexpected return code " + str(prog._pid.returncode)
        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, "utf-8")
        msg.attach(MIMEText(text, _charset="utf-8"))

        try:
            mailServer = smtplib.SMTP("smtp.gmail.com", 587)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.login(self._myaddr, self._myaddr_pswd)
            mailServer.sendmail(self._myaddr, self._toaddr, msg.as_string())
            mailServer.close()
        except:
            return 1
        return 0