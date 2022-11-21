#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=backend \
SMTP_HOST="" \
TRAEFIK_PUBLIC_NETWORK_IS_EXTERNAL=false \
INSTALL_DEV=true \
docker-compose \
-f docker-compose.yml \
config > docker-stack.yml

printf "before docker stuff \n"
docker-compose -f docker-stack.yml build
printf "after build \n"
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
printf "after down \n"
docker-compose -f docker-stack.yml up -d
printf "after up \n"
docker-compose -f docker-stack.yml ps
docker-compose -f docker-stack.yml exec -T backend bash /app/tests-start.sh "$@"
printf "after exec \n"
docker-compose -f docker-stack.yml down -v --remove-orphans
