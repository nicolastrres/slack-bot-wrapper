#!/usr/bin/env bash

. ./scripts/print.sh
. ./scripts/standup_example.sh
. ./scripts/tests.sh

function _help() {
  echo_in_yellow "t|tests               Run all tests."
  echo_in_yellow "e|example             Run standup example."
}

if [ -z ${1} ];then
    _help
else
  case ${1} in
    t|tests)
      tests
    ;;
    e|example)
      start_example
    ;;
    *)
      if [ ! -z ${1} ];then
        echo_in_red "'${1}' not found"
        _help
      fi
    ;;
  esac
fi