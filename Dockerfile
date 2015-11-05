FROM python:2-onbuild
MAINTAINER Alex Lee <lilu@mequanta.com>
EXPOSE 8000
CMD [ "python", "./dyno.py" ]