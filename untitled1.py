# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 06:39:58 2022

@author: karan.rana
"""

import smtplib
from email.message import EmailMessage
import ssl


sender = 'karanid420@gmail.com'
receivers = 'karan'
password = 'knllhltkgtghhyik'
Subject= 'SMTP e-mail test'

message = """From: From Person <from@karan.rana@ariespro.com>
To: To Person <to@aishwarya.jadhav@ariespro.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

server=EmailMessage()

server['From']=sender
server['To']=receivers
server['Subject']=Subject
server.set_content(message)

context=ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com',465,context) as smtp:
    smtp.login(sender,password)
    smtp.sendmail(sender,receivers,server.as_string())


print ("Successfully sent email")
