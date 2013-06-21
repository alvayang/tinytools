tinytools
=========

Common Tools

### usage

#### dynamic_domain.py
用来动态绑定[dnspod](https://www.dnspod.cn/)的域名。  
使用时，修改用户名，密码，相应的域名，执行即可。  
找到下面几行，分别修改为对应的参数：  

```
    ('login_email', '##ADD YOUR EMAIL ###') ####修改
    ('login_password', '##ADD YOUR PASSWORD ####') ####修改
    dip = DynaticIP(domain_change = ['#要修改的Domain列表#', '#又一个要修改的域名#', 'facealfa.com', 'facealpha.com'])
```
