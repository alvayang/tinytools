#!/bin/env python
#coding:utf-8
'''
* 这个文件用于修改dnspod中A名称为*和@的ip，工作原理：
     1. 先去ip138取一下自己的地址
     2. 和文件中保存的上次的ip地址比对
     2.1 如果没变化，则退出
     2.2 如果发生变化，则取指定用户名下的domain的列表
     3. 在2.2的基础上，找到要修改的域名的id，获取record为*和@的A记录对应的recordid
     4. 在3的基础上，修改这些对应的recordid所对应的ip地址为1中获取的值


* Test@ ubuntu 12.10  3.5.0-34-generic #55-Ubuntu SMP Thu Jun 6 20:20:19 UTC 2013 i686 i686 i686 GNU/Linux

* @author alvayang <netyang@gmail.com>
* @date   Fri Jun 21 18:20:10 2013

'''

from poster.encode import multipart_encode
from tornado.httpclient import HTTPRequest, HTTPClient
import sys,uuid, traceback,cjson
from BeautifulSoup import BeautifulSoup

class DynaticIP:
    def __init__(self, sleep = 60, domain_change = ''):
        self._lastip = None
        self._sleep = sleep
        self.common = [
            ('login_email', '##ADD YOUR EMAIL ###') ####修改
            ,('login_password', '##ADD YOUR PASSWORD ####') ####修改
            ,('format', 'json')
            ,('lang', 'cn')
            ,('error_on_empty', 'no')
            ]
        self.__domain_want = domain_change
        self.__domains = {}
        
    def debug(self, msg):
        print msg

    def check_domain_list(self):
        url = 'https://dnsapi.cn/Domain.List'
        _param = self.common
        _param.append(('type', 'all'))
        (s, obj) = self.__post_common(url, _param)
        if s:
            domains = obj['domains']
            for x in domains:
                self.__domains[x['name']] = x['id']
        else:
            pass

    def __change_ip(self):
        self._c_record_ids = []
        if self._lastip:
            _domain_keys = self.__domains.keys()
            for x in self.__domain_want:
                if x in _domain_keys:
                    # 修改一下
                    self.__check_record(self.__domains[x])

    def __update_record(self, domain_id, record_id, subdomain):
        url = 'https://dnsapi.cn/Record.Modify'
        _param = self.common
        _param.append(('domain_id', domain_id))
        _param.append(('record_id', record_id))
        _param.append(('sub_domain', subdomain))
        _param.append(('record_type', 'A'))
        _param.append(('record_line', u'默认'))
        _param.append(('value', '%s' % self._lastip))
        _param.append(('mx', '1'))
        _param.append(('ttl', '120'))
        (s, obj) = self.__post_common(url, _param)
        if s:
            print "update success: %s, %s, %s" % (domain_id, record_id, subdomain)
        

    def __check_record(self, domain_id):
        url = 'https://dnsapi.cn/Record.List'
        _param = self.common
        _param.append(('domain_id', domain_id))
        (s, obj) = self.__post_common(url, _param)
        if s:
            for x in obj['records']:
                if x['type'] == 'A' and x['name'] in ('*', '@'):
                    self.__update_record(domain_id, x['id'], x['name'])
        
    def run(self):
        self._lastip = self.__check_ip()
        if self._lastip == "": return
        _ip = ''
        try:
            with open('/opt/scripts/.lastip', 'r') as f:
                _ip = f.readline().strip()
        except:
            pass
            
        if _ip ==  self._lastip:
            return

        with open('/opt/scripts/.lastip', 'w') as f:
            print >> f, self._lastip

        # while 1:
        #     _ip = self.__check_ip()
        #     if self._lastip != _ip:
        #         self._lastip = _ip
        #         print "Update DNSPOD"
        #     else:
        #         print "No Need To"
        #     time.sleep(self._sleep)
        self.check_domain_list()
        self.__change_ip()


    def __post_common(self, url, param):
        buf = ''
        try:
            buf = self.__do_post(url, param)
        except:
            self.debug(traceback.format_exc())
            return (False, {})
        try:
            obj = cjson.decode(buf)
        except:
            self.debug(traceback.format_exc())
            return (False, {})

        return (int(obj['status']['code']) == 1, obj)


    def __check_ip(self):
        _url = 'http://iframe.ip138.com/ic.asp'
        _ipbuf = self.__do_get(_url)
        bs = BeautifulSoup(_ipbuf)
        t = bs.find('center').getString().encode('UTF-8')
        return (t.split("]")[0]).split("[")[1]


    def __do_get(self, _url):
        client = HTTPClient()
        request = HTTPRequest(_url, method = 'GET')
        response = client.fetch(request)
        data = response.body
        _buf = data.decode('GB2312').encode('UTF-8')
        return _buf

    def __do_post(self, _url, _form = []):
        data_gen, header = multipart_encode(_form)
        client = HTTPClient()
        request = HTTPRequest(_url, method = 'POST', body = ''.join(data_gen), headers = header)
        response = client.fetch(request)
        data = response.body
        return data

if __name__ == "__main__":
    dip = DynaticIP(domain_change = ['#要修改的Domain列表#', '#又一个要修改的域名#', 'facealfa.com', 'facealpha.com'])
    dip.run()
