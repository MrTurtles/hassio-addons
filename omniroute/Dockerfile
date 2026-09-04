FROM node:22-alpine

RUN npm install -g omniroute

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
