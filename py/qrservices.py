#!/bin/env python
#-*- coding:utf-8 -*-
import bjoern
import urlparse
import traceback
from cgi import FieldStorage
import os.path
import logging
import StringIO
import urllib2
from PIL import Image

import qrcode

def start():

    def generage_qr(environ, start_response):
        if environ['REQUEST_METHOD'].lower() == "get":
            start_response('200 OK', [('Content-Type','text/html')])
            return """
                <?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        
                <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
                <head>
                      <meta content="text/html; charset=utf-8" http-equiv="content-type"/>
                </head>
                <body>
                <form action='/qr/' method='post'>
                    <p><input type='text' style='width:200px;height:30px;font-size:17px;' placeholder='内容' name='url' ></p>
                    <p><input type='text' style='width:200px;height:30px;font-size:17px;' placeholder='中心图' name='tiny' ></p>
                    <p><input type='submit' value='Generate'></p>
                </form>
                </body>
                </html>
                """
        else:
            form = FieldStorage(fp=environ['wsgi.input'], environ=environ)
            _url = form['url'].value
            _tiny = ''
            if form.has_key('tiny'):
                _tiny = form['tiny'].value or ''
            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.ERROR_CORRECT_H,
                box_size=10,
                )
            qr.make(fit=True)
            qr.add_data(_url)
            img = qr.make_image()
            err = ""
            if _tiny.startswith('http'):
                try:
                    _buf = urllib2.urlopen(_tiny).read()
                    _t_im = Image.open(StringIO.StringIO(_buf))
                    #//_t_im.verify()
                    s = img.size
                    print _t_im, _t_im.size, s
                    t = (int(s[0] / 5), int(s[1] / 5))
                    _t_im = _t_im.resize(t)
                    img.paste(_t_im, ((s[0] - (s[0] / 5))/2, (s[1] - (s[1] / 5))/2))
                except:
                    print traceback.format_exc()
                    err = '打开远程文件出错'
                    pass
            output = StringIO.StringIO()
            img.save(output, 'PNG')
            contents = output.getvalue().encode("base64")
            output.close()
            start_response('200 OK', [('Content-Type','text/html')])
            return """
                <?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        
                <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
                <head>
                      <meta content="text/html; charset=utf-8" http-equiv="content-type"/>
                </head>
                <body>
                <form action='/qr/' method='post'>
                    <p><input type='text' style='width:200px;height:30px;font-size:17px;' placeholder='内容' name='url' ></p>
                    <p><input type='text' style='width:200px;height:30px;font-size:17px;' placeholder='中心图' name='tiny' ></p>
                    <p><input type='submit' value='Generate'></p>
                </form>
                <hr>
                %s
                <hr>
                <img style="width:600px;height:600px"src='data:image/png;base64,%s' />"
                </body>
                </html>
                """ % (err, contents)

    dispatch = {
        '/': generage_qr
    }
           
    def choose(environ, start_response):
        return dispatch.get(environ.get('PATH_INFO'), generage_qr)(environ, start_response)
    bjoern.run(choose, '0.0.0.0', 9002)


if __name__ == "__main__":
    start()
