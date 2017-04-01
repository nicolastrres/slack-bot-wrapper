#!/usr/bin/env bash

function echo_in_red() { echo -e "'\033[0;31m${1}\033[m"; }
function echo_in_green() { echo -e "\033[0;32m${1}\033[m"; }
function echo_in_yellow() { echo -e "\033[0;33m${1}\033[m"; }
function echo_underlined() { echo -e "\033[4;31m${1}\033[m"; }
