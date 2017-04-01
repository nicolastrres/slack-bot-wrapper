#!/usr/bin/env bash

. ./scripts/print.sh
. ./scripts/tests.sh

function _help() {
    echo_in_yellow "t|tests               Run all tests."
}


if [ -z ${1} ];then
    _help
else
  case ${1} in
    t|tests)
      tests
    ;;
    *)
      if [ ! -z ${1} ];then
        echo_in_red "'${1}' not found"
        _help
      fi
    ;;
  esac
fi