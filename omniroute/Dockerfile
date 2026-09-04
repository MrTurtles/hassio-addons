ARG BUILD_FROM
FROM $BUILD_FROM

RUN npm install -g omniroute

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
