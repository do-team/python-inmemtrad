FROM alpine:3.3

# Prepare env
RUN apk add --update python
RUN mkdir -p /usr/src/inmemtrad
WORKDIR /usr/src/inmemtrad

# Install app
COPY inmemtrad.py /usr/src/inmemtrad
COPY . /usr/src/inmemtrad

RUN pip install redis

CMD ["python", "inmemtrad.py", "", "10000000"]