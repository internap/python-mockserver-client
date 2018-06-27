#!/bin/bash -ex

teardown() {
    docker-compose down
}

docker-compose up -d

trap teardown INT TERM EXIT

show_failures() {
    docker-compose logs --timestamps mock-server
    exit 1
}

nosetests --verbose --detailed-errors --debug=DEBUG || show_failures

