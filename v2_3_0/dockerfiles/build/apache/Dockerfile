FROM php:7.2.15-fpm

MAINTAINER "Magento"

ENV PHP_EXTRA_CONFIGURE_ARGS="--enable-fpm --with-fpm-user=magento2 --with-fpm-group=magento2"

RUN apt-get update && apt-get install -y \
    apt-utils \
    sudo \
    unzip \
    cron \
    curl \
    libmcrypt-dev \
    libicu-dev \
    libxml2-dev libxslt1-dev \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    git \
    supervisor \
    mysql-client \
    ocaml \
    expect \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-configure hash --with-mhash \
    && docker-php-ext-install -j$(nproc) intl xsl gd zip pdo_mysql opcache soap bcmath json iconv \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && apt-get clean && apt-get update && apt-get install -y curl gnupg2 software-properties-common \
    && curl -sL https://deb.nodesource.com/setup_11.x | sudo bash - \
    && apt-get update && apt-get install -y nodejs

RUN  npm update -g npm && npm install -g grunt-cli && npm install -g gulp \
    && echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config \
    && apt-get install -y apache2 \
    && a2enmod rewrite \
    && a2enmod proxy \
    && a2enmod proxy_fcgi \
    && a2enmod ssl \
    && rm -f /etc/apache2/sites-enabled/000-default.conf \
    && groupadd -r -g 2000 magento2 \
    && useradd -u 2000 -g 2000  -m -d /home/magento2 -s /bin/bash magento2 && adduser magento2 sudo \
    && echo "magento2 ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && touch /etc/sudoers.d/privacy \
    && echo "Defaults        lecture = never" >> /etc/sudoers.d/privacy \
    && mkdir /home/magento2/magento2 && mkdir /var/www/magento2 \
    && mkdir /home/magento2/state \
    && curl -sS https://accounts.magento.cloud/cli/installer -o /home/magento2/installer \
    && rm -r /usr/local/etc/php-fpm.d/* \
    && sed -i 's/www-data/magento2/g' /etc/apache2/envvars

# PHP config
COPY config/php.ini /usr/local/etc/php

# supervisord config
COPY config/supervisord.conf /etc/supervisord.conf

# php-fpm config
COPY config/php-fpm-magento2.conf /usr/local/etc/php-fpm.d/php-fpm-magento2.conf

# apache config
COPY config/apache-default.conf /etc/apache2/sites-enabled/apache-default.conf
COPY config/entrypoint.sh /usr/local/bin/entrypoint.sh

ENV PATH $PATH:/home/magento2/scripts/:/home/magento2/.magento-cloud/bin
ENV PATH $PATH:/var/www/magento2/bin

ENV USE_SHARED_WEBROOT 1
ENV SHARED_CODE_PATH /var/www/magento2
ENV WEBROOT_PATH /var/www/magento2
ENV MAGENTO_ENABLE_SYNC_MARKER 0

WORKDIR /var/www
RUN curl -LO https://github.com/magento/magento2/archive/2.3.0.tar.gz
RUN tar xzvf /var/www/2.3.0.tar.gz -C /var/www/ \
    && mv /var/www/magento2-2.3.0/* /var/www/magento2 \
    && ls -la /var/www/magento2

WORKDIR /var/www/magento2
RUN composer install

# Initial scripts
COPY scripts /home/magento2/scripts/
RUN cd /home/magento2/scripts && composer install && chmod +x /home/magento2/scripts/m2init

RUN chown -R magento2:magento2 /home/magento2 && \
    chown -R magento2:magento2 /var/www/magento2 && \
    chmod 755 /home/magento2/scripts/bin/magento-cloud-login

#Change access righs to conf, logs, bin from root to www-data
#setcap to bind to privileged ports as non-root
RUN chown -hR magento2:magento2 /etc/apache2 && \
    mkdir -p /var/run/apache2/ && \
    chown -R magento2. /var/log/apache2/ && \
    chown -R magento2. /var/run/apache2/ && \
    setcap 'cap_net_bind_service=+ep' /usr/sbin/apache2 && \
    getcap /usr/sbin/apache2 && \
    chown -hR magento2:magento2 /usr/local/var

EXPOSE 80
WORKDIR /home/magento2
USER magento2

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
