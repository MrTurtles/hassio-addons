ARG BUILD_FROM
FROM $BUILD_FROM

# OmniRoute needs Node >=22 <23 or >=24 <27 (Node 23 is explicitly excluded)
RUN apk add --no-cache nodejs npm \
    && npm install -g omniroute

COPY run.sh /etc/services.d/omniroute/run
RUN chmod a+x /etc/services.d/omniroute/run
