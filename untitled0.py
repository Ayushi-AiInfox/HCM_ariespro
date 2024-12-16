# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 04:54:26 2022

@author: karan.rana
"""

#!/usr/bin/python

import smtplib

server=smptlib.SMTP('smtp.gmail.com',587)

server.starttls()

sender = 'karanid420@gmail.com'
receivers = ['kccse.ranaji@gmail.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""


smtpObj = smtplib.SMTP('localhost')
smtpObj.sendmail(sender, receivers, message)         
print ("Successfully sent email")
