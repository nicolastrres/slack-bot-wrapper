#!/usr/bin/env bash

set -e

function create_docker_image_if_does_not_exist() {
  if ! docker images | grep -w "nicolastrres/slack-bot" &> /dev/null ; then
    echo_in_green "No image found for nicolastrres/slack-bot"
    echo_in_green "Creating new image"
    docker build . -t nicolastrres/slack-bot
  fi
}

function tests() {
  create_docker_image_if_does_not_exist
  docker run --rm -v $(pwd):/slack-bot nicolastrres/slack-bot py.test tests
  echo_in_green "Unit tests passed"
}