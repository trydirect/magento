
![Docker Stars](https://img.shields.io/docker/stars/trydirect/magento.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/trydirect/magento.svg)
![Docker Automated](https://img.shields.io/docker/cloud/automated/trydirect/magento.svg)
![Docker Build](https://img.shields.io/docker/cloud/build/trydirect/magento.svg)

# Magento Docker build files

This repo contains Magento docker build files for different versions of Magento


### Installing

```
1. Clone repository
2. cd magento/<version>/dockerfiles 

Find .env file open it with editor and replace all vars wrapped with {{var}} .  
Example: DB_USER: {{DB_USER}} to  DB_USER:magento

3. docker-compose up -d 
```

## Built With

* [PHP](http://www.php.net) - PHP 
* [Nginx](https://nginx.org/) - Web server
* [MySQL](https://www.mysql.com/) - Database engine

## Getting Started

Example docker-compose.yml file:

```
version: '2'

volumes:
  mariadb_data:
    driver: local
  magento_data:
    driver: local

services:
  magento:
    image: ${REGISTRY}trydirect:magento:2.3.2
    container_name: magento
    env_file:
      .env
    volumes:
      - ./magento:/home/magento2   
      - /var/www
      - magento_data:/data
      - ./cron:/var/spool/cron/crontabs
    depends_on:
      - mariadb
    working_dir:  /var/www/magento2

  mariadb:
    image: "mariadb:latest"
    container_name: magento_mariadb
    env_file:
      .env
    volumes:
      - "mariadb_data:/var/lib/mysql"

  nginx:
    image: ${REGISTRY}nginx-le:stable
    container_name: nginx
    env_file: .env
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./certs/ssl:/etc/ssl/nginx
      - ./certs/letsencrypt:/etc/letsencrypt
      - ./cron/nginx:/var/spool/cron/crontabs
      - ./nginx/conf.d:/etc/nginx/conf.d/
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./null:/etc/nginx/sites-enabled
      - ./supervisord/nginx.conf:/etc/supervisor/conf.d/nginx.conf
    links:
      - magento
    entrypoint: /usr/bin/supervisord -c /etc/supervisor/supervisord.conf -n

```


## Contributing

Join https://gitter.im/try-direct/community for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

See the list of [contributors](https://github.com/trydirect/magento/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## How to mount magento from host machine

Add 
``` 
volumes:
      - ./magento:/var/www/magento2
```
to magento service in case you have magento source code on your host machine and want to sync directories with container.

