#Descargamos y trabajaremos directamente en python en la versión 3.9,
#tomando como base la distribución Linux Alpine
FROM python:3.9

#
RUN pip install mysql-connector-python

WORKDIR /usr/app/src

RUN mkdir programas

COPY ./util/*.py ./programas

RUN mkdir archivos
RUN mkdir copias

COPY archivos_ejemplos/ /usr/app/src/archivos/
