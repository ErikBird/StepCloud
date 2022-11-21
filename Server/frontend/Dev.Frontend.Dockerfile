# Vue
FROM node:12.18.0-alpine as build-vue
WORKDIR /app/client
ENV PATH /app/node_modules/.bin:$PATH
ARG VUE_APP_API_DOMAIN
ENV VUE_APP_API_DOMAIN=$VUE_APP_API_DOMAIN
COPY ./frontend/package.json ./
RUN npm install
COPY ./frontend .
