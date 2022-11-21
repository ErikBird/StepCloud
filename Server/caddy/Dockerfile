# build
FROM docker.io/library/node:12.16.1-alpine as build-vue
WORKDIR /app/server
ENV PATH /app/server/node_modules/.bin:$PATH
ARG VUE_APP_ENV
ENV VUE_APP_ENV=$VUE_APP_ENV
COPY ./frontend/package*.json ./

RUN npm install --loglevel verbose
COPY ./frontend .
RUN npm run build

# note: never use the :latest tag in a production site
FROM docker.io/library/caddy
ARG CADDY_FILE
COPY $CADDY_FILE /etc/caddy/Caddyfile
COPY --from=build-vue /app/server/dist ./
