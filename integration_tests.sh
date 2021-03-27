#!/bin/bash

APP_PATH=/home/user/Documents/FlagScraper
rm -rf /tmp/flagscraper
mkdir -p /tmp/flagscraper/
export LOCAL_DATA_PATH=/tmp/flagscraper

export Q_HOST=172.17.0.3
export Q_LOGIN=test
export Q_PASSWD=test
export DB_HOST=172.17.0.2
export DB_LOGIN=test
export DB_PASSWD=test

# services=["LinkParser"] # probably not for integration tests, eh?
for service in ${services[@]}; do

    cp -r $APP_PATH/$service/test/test_data/* /tmp/flagscraper/

    docker run -d \
    -v $LOCAL_DATA_PATH/mysql:/var/lib/mysql \
    mysql:5.7

    docker run -d \
    --network test-rabbitmq-net \
    --ip 172.19.0.2 \
    -p 15672:15672 \
    flag-scraper.test.rabbitmq

    source $APP_PATH/.venv/bin/activate
    python3 -m unittest discover $APP_PATH/$service/test "test_*.py"

    docker container rm -f flag-scraper.test.rabbitmq flag-scraper.test.mysql
    docker network rm test-rabbitmq-net
done

