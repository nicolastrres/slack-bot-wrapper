#!/usr/bin/env bash

function start_example() {
  docker run --rm -v $(pwd):/slack-bot --env-file .env nicolastrres/slack-bot python3 -m examples.standup_bot
}