FROM python:3
ENV TERM=xterm-256color
ENV PYTHONPATH=.

WORKDIR /usr/src/app

COPY . .
RUN make requirements

CMD [ "make", "test" ]
