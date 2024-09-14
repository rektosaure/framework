#!/bin/bash

do_start() {
  echo -e "\nDocker > Starting ITPM utility ..."
  systemctl is-active --quiet docker || systemctl --user start docker
  docker compose -f docker-compose.yaml up -d
  echo "http://localhost:1337/swagger"
}

do_stop() {
  echo -e "\nDocker > Stopping ITPM utility ..."
  docker compose -f docker-compose.yaml down
  systemctl --user stop docker
}

do_update() {
  echo -e "\nDocker > Updating ITPM utility ..."
  systemctl is-active --quiet docker || systemctl --user start docker
  docker compose -f docker-compose.yaml pull
}

case "$1" in
  start)
    do_start
    ;;
  stop)
    do_stop
    ;;
  update)
    do_update
    ;;
  *)
    echo "Usage: itpm.bash {start|stop|update}"
    exit 1
esac

exit 0
