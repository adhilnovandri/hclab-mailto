import smtplib, os, json, cx_Oracle
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from PyPDF2 import PdfFileReader, PdfFileWriter


class Mailto:
    def __init__(self,mailaddr,labno):
        with open(os.path.join(os.getcwd(),'application.json'),'r') as f:
            setting = json.load(f)
        
        #get email configuration
        self.mail_host = setting['mail']['host']
        self.mail_port = setting['mail']['port']
        self.mail_name = setting['mail']['from']['name']
        self.mail_addr = setting['mail']['from']['address']
        self.mail_subject = setting['mail']['subject']
        self.mail_usr = setting['mail']['username']
        self.mail_psw = setting['mail']['password']
        self.mail_psw = setting['mail']['password']
        self.mail_atch = setting['mail']['attachment_path']

        self.mailaddr = mailaddr
        self.labno = labno

    def encrypt_attachment(self,filename):
        password_pdf = '12345678'
        #password_pdf = self.getPassword()

        with open(os.path.join(self.mail_atch,filename), "rb") as in_file:
            input_pdf = PdfFileReader(in_file)
            output_pdf = PdfFileWriter()
            output_pdf.appendPagesFromReader(input_pdf)
            
            output_pdf.encrypt(password_pdf)

            with open(os.path.join(self.mail_atch,'encrypted',filename), 'wb') as out_file:
                    output_pdf.write(out_file)


    def sendEmail(self):
        
        #setup mail header
        msg = MIMEMultipart()
        msg['From'] = self.mail_name
        msg['To'] = self.mail_addr
        msg['Subject'] = self.mail_subject

        #setup mail body
        with open(os.path.join(os.path.dirname(__file__),'body.html'),'r') as f:
            body = f.read()
        msg.attach(MIMEText(body, 'html'))

        filename = str(self.labno) + '.pdf'
        self.encrypt_attachment(filename)
        print(os.path.join(self.mail_atch,'encrypted',filename))
        attachment = open(os.path.join(self.mail_atch,'encrypted',filename),'rb')
        p = MIMEBase('application','octet-stream')
        p.set_payload(attachment.read())

        encoders.encode_base64(p)
        p.add_header('Content-Disposition',f'attachment; filename={filename}')
        msg.attach(p)

        content = msg.as_string()

        server = smtplib.SMTP(self.mail_host,self.mail_port)
        server.starttls()
        server.login(self.mail_usr,self.mail_psw)
        server.sendmail(from_addr=self.mail_addr,to_addrs=self.mailaddr,msg=content)

if __name__ == '__main__':
    m = Mailto('adhil.nvndr@gmail.com','144651')
    m.sendEmail()