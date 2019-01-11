
MAGENTO with sample data will be created as a separate stack because of complexity


login with app user
create auth.json
Public Key: bbf2a594dc3d5d1f57276138e9c7c457
Private Key: c39a165334582213e73f2477d4f6808e

{agento2@f4553b3dad59:/var/www/magento2$ cat /home/magento2/.composer/auth.json
  "http-basic": {
     "repo.magento.com": {
        "username": "bbf2a594dc3d5d1f57276138e9c7c457",
        "password": "c39a165334582213e73f2477d4f6808e"
     }
  }

cd /var/www
composer create-project https://repo.magento.com/ magento/project-community-edition magento2

php bin/magento setup:install --base-url=http://dinelo.com --db-host=mariadb --db-name=magento2 --db-user=magento2 --db-password=6nMfTrhM --admin-firstname=Magento --admin-lastname=User --admin-email=user@example.com --admin-user=admin --admin-password=admin2018 --language=en_US --currency=USD --timezone=America/Chicago --use-rewrites=1 --backend-frontname=admindashboard

bin/magento sampledata:deploy
bin/magento setup:upgrade




The file "/var/www/magento2/generated/code/Dotdigitalgroup/Email/Model/Connector/AccountFactory.php" cannot be deleted Warning!unlink(/var/www/magento2/generated/code/Dotdigitalgroup/Email/Model/Connector/AccountFactory.php): Permission denied


SetEnvIf X-Forwarded-Proto https HTTPS=on
magento ssl loop

this piece of code should be added to index.php

if ($http_x_forwarded_proto = "https") {
   set $my_http "https";
   set $my_ssl "on";
   set $my_port "443";
 }