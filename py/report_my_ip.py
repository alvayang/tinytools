#!/bin/env python


# /**
# * @file   report_my_ip.py
# * @author Yang.Song <netyang@gmail.com>
# * @date   Mon Apr  1 16:07:44 2013
# * 
# * @brief  
# * 
# * 
# */

import urllib, sys, os, os.path
import marshal, hashlib


import smtplib


def send_email_163(from_addr = 'wantmyip@163.com', 
                   password = 'wantmyip123123', 
                   to_addrs = ('wantmyip@163.com'), 
                   subject = 'Your IP, My lord.', 
                   content = None 
                   ): 

    if content is None: 
        print 'content is None.' 
        return False 
    try: 
        from smtplib import SMTP 
        from email.mime.text import MIMEText 

        email_client = SMTP(host = 'smtp.163.com') 
        email_client.login(from_addr, password) 

        #create msg 
        msg = MIMEText(content, _charset = 'utf-8') 
        msg['Subject'] = subject 
        email_client.sendmail(from_addr,to_addrs, msg.as_string()) 
        return True 

    except Exception,e: 
        print e 
        return False 
    finally: 
        email_client.quit() 

opener = urllib.urlopen("http://a.ku6.com/z/i.php")
data = ''.join(opener.readlines())
z = hashlib.md5(data).hexdigest()
l = ''

if os.path.exists('lastip'):
    with open('lastip', 'r') as f:
        l = ''.join(f.readlines())
if str(l).strip() == str(z).strip():
    sys.exit(0)
else:
    with open('lastip', 'w') as f:
        print >> f, z

    send_email_163(content = str(data))

    


    
