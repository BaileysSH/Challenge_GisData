FROM --platform=linux/amd64/v8 mysql:5.7

ENV MYSQL_ROOT_PASSWORD=toor
ENV MYSQL_DATABASE=batch
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=resu

ADD schema.sql /docker-entrypoint-initdb.d
EXPOSE 3306