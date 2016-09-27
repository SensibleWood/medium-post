#!/usr/bin/env bash

# Description: Simple script to start application

script_dir=$(dirname $0)
crypto_dir=${script_dir}/../crypto

if [[ ! -f ${crypto_dir}/server.key ]] ; then
    mkdir $crypto_dir && \
    openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout $crypto_dir/server.key -out $crypto_dir/server.crt
fi

# Start the python application
python $script_dir/../app.py