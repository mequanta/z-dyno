FROM python:2-onbuild
MAINTAINER Alex Lee <lilu@mequanta.com>
EXPOSE 5000
CMD [ "python", "./tornado_server.py" ]