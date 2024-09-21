#!/usr/bin/env bash
set -e

host="$1"
shift
port="$1"
shift

while ! nc -z "$host" "$port"; do
  sleep 1
done

exec "$@"
