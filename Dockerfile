FROM selenium/standalone-chrome:104.0

COPY requirements.txt /

USER root
RUN apt update && apt install --yes python3-pip

RUN pip3 install -r /requirements.txt

COPY src /termin
WORKDIR /termin

ENV TERMIN_ROOT=/var
CMD python3 main.py
