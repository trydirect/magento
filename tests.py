#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import docker
import requests

client = docker.from_env()

# Testing Magento build

time.sleep(20)  # we expect all containers are up and running in 20 secs

for c in client.containers.list():
    print("{}: {}" .format(c.name, c.status))
    if 'running' not in c.status:
        print(c.logs())

# # NGINX
nginx = client.containers.get('nginx')
nginx_cfg = nginx.exec_run("/usr/sbin/nginx -T")
assert nginx.status == 'running'
assert 'server_name _;' in nginx_cfg.output.decode()
assert "error_log /proc/self/fd/2" in nginx_cfg.output.decode()
assert "location = /.well-known/acme-challenge/" in nginx_cfg.output.decode()
assert 'HTTP/1.1" 500' not in nginx.logs()

# Apache
apache = client.containers.get('magento')
cfg = apache.exec_run("apachectl -t")
print(cfg.output.decode())
assert apache.status == 'running'
print(apache.logs())
assert 'HTTP/1.1" 500' not in apache.logs()
# test restart
apache.restart()
time.sleep(3)
assert apache.status == 'running'
print(apache.logs())

# PHP-APACHE2
php = client.containers.get('magento')
php_log = php.logs()
assert php.status == 'running'
print(php_log.decode())
apache_proc = php.exec_run("sh -c 'ps aux|grep apache2'")
print(apache_proc.output.decode())
assert 'apache2 -D FOREGROUND' in apache_proc.output.decode()
ss = php.exec_run("sh -c 'ss -tlpn'")
assert '*:80' in ss.output.decode()

db = client.containers.get('magento_mariadb')
assert db.status == 'running'
cnf = db.exec_run("/usr/sbin/mysqld --verbose  --help")
assert 'mysqld  Ver 5.7' in cnf.output.decode()
db_log = db.logs()
assert "mysqld: ready for connections" in db_log.decode()

# check redirect to web installer
curl = php.exec_run("curl -i http://localhost")
print(curl.output.decode())
# assert 'Location: http://localhost/index.php/installer' in curl.output.decode()
# @todo run magento unit test, first copy .env.dist to .env
#php_conf = php.exec_run("bin/phpunit --bootstrap vendor/autoload.php --configuration app/phpunit.xml.dist")

