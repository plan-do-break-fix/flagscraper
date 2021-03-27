#!/bin/bash

APP_PATH=/home/user/Documents/FlagScraper
export CONTAINER_DATA_PATH=/tmp/flagscraper
export IDLE_TIME=30

services=("LinkParser" "Abstract")
for service in ${services[@]}; do

    printf "\nTesting $service\n"

    rm -rf /tmp/flagscraper
    mkdir /tmp/flagscraper/
    cp -r $APP_PATH/$service/test/test_data/* $CONTAINER_DATA_PATH

    source $APP_PATH/.venv/bin/activate
    python3 -m unittest discover $APP_PATH/$service/test "test_*.py"

done

