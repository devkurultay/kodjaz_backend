#!/bin/bash

sed_args=( -i )

# Make sed options macos compatible
if [[ $OSTYPE == 'darwin'* ]];
    then sed_args=( -i '' -e)
fi

# Load variables form .env file
source .env

# replace values in .env file for prod
sed "${sed_args[@]}" "s/DEBUG=True/DEBUG=False/g" .env
# # '#' is a delimiter here 
sed "${sed_args[@]}" "s#$API_URL_ROOT#https://$BACKEND_URL_ROOT/api/#g" .env
sed "${sed_args[@]}" "s#$DJANGO_SETTINGS_MODULE#config.settings_prod#g" .env
