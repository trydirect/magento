#!/usr/bin/env bash

rm -rf /var/www/magento2/status.html
rm -rf /home/magento2/magento2/status.html
supervisord -n -c /etc/supervisord.conf
