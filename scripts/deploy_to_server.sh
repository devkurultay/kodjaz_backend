#!/bin/bash

# This script depends on the buildreact-prod step
# Make sure to use `make deploy` command
echo "Activating virtual env"
source env/bin/activate

echo "Collecting static files"
# python manage.py collectstatic --noinput --settings=config.settings_prod
# Bundle up an archive file. Include staticfiles/ if you are not using AWS S3
echo "Creating an archive"
tar -cf kodjaz.tar --exclude='frontend/node_modules/*' scripts/ authentication/ config/ courses/ fixtures/ frontend/ server_configs/ requirements/ users/ manage.py robots.txt .env
# Load variables form .env file
echo "Loading env variables"
source .env
# Upload bundled archive
ssh -tt $SERVER_USERNAME@$SERVER_IP << END
    if [ ! -d /home/$SERVER_USERNAME/$PROJECT_FOLDER_ON_SERVER ]; then
        mkdir /home/$SERVER_USERNAME/$PROJECT_FOLDER_ON_SERVER;
    fi
    if [ ! -d /home/$SERVER_USERNAME/$PROJECT_FOLDER_ON_SERVER/logs ]; then
        mkdir /home/$SERVER_USERNAME/$PROJECT_FOLDER_ON_SERVER/logs;
        touch /home/$SERVER_USERNAME/$PROJECT_FOLDER_ON_SERVER/logs/access.log;
        touch /home/$SERVER_USERNAME/$PROJECT_FOLDER_ON_SERVER/logs/error.log;
    fi
    exit
END

scp kodjaz.tar $SERVER_USERNAME@$SERVER_IP:$PROJECT_FOLDER_ON_SERVER/
rm kodjaz.tar
ssh -tt $SERVER_USERNAME@$SERVER_IP << END
    cd $PROJECT_FOLDER_ON_SERVER/
    echo "Clearing static files folder"
    rm -rf staticfiles/
    
    echo "Unpacking"
    tar -xf kodjaz.tar

    # replace values in .env file
    chmod +x scripts/replace_env_values_for_prod.sh
    ./scripts/replace_env_values_for_prod.sh

    # replace values in config files
    sed -i 's/example.com/$BACKEND_URL_ROOT/' $NGINX_CONFIG_FILE_NAME
    sed -i 's/0.0.0.0/$SERVER_IP/' $NGINX_CONFIG_FILE_NAME
    sed -i 's/username/$SERVER_USERNAME/' $NGINX_CONFIG_FILE_NAME
    sed -i 's/username/$SERVER_USERNAME/' $SERVICE_CONFIG_FILE_NAME
    sed -i 's/backend_folder/$PROJECT_FOLDER_ON_SERVER/' $NGINX_CONFIG_FILE_NAME
    sed -i 's/backend_folder/$PROJECT_FOLDER_ON_SERVER/' $SERVICE_CONFIG_FILE_NAME
    sed -i 's/example_sock/$SOCKET_NAME/' $NGINX_CONFIG_FILE_NAME
    sed -i 's/example_sock/$SOCKET_NAME/' $SERVICE_CONFIG_FILE_NAME
    sed -i 's/example_sock/$SOCKET_NAME/' $SOCKET_CONFIG_FILE_NAME
    sed -i 's/example_pid/$PID_FILE/' $SERVICE_CONFIG_FILE_NAME

    source env/bin/activate && echo 'Activated env' || echo $SERVER_PASS sudo -S apt install python3.8-venv --yes && python3 -m venv env && source env/bin/activate && echo 'Installed and activated env';
    echo "Now installing python packages"
    pip install --upgrade pip
    pip install -r requirements/requirements_prod.txt
    echo "Applying migrations"
    python manage.py migrate --noinput --settings=config.settings_prod
    echo $SERVER_PASS sudo -S systemctl daemon-reload
    echo $SERVER_PASS sudo -S systemctl reload gunicorn_kodjaz.service
    echo $SERVER_PASS sudo -S systemctl daemon-reload
    echo $SERVER_PASS sudo -S systemctl reload nginx
    echo "Exiting"
    exit
END
