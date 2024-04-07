FROM python:3.11.5-alpine

COPY . /app/

RUN set -eux \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apk update \
    && apk add --no-cache iptables \
    && iptables -A INPUT -p tcp --dport 8080 -j ACCEPT \
    && iptables -A INPUT -p tcp --dport 80 -j ACCEPT \
    && iptables -A INPUT -p tcp --dport 443 -j ACCEPT \
    && iptables -A OUTPUT -p tcp --dport 8080 -j ACCEPT \
    && iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT \
    && iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT \
    && apk del --purge .build-deps \
    && rm -rf /var/cache/apk/*

EXPOSE 5000 443 8080 80

CMD python /app/app.py