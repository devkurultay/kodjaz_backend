#!/bin/bash
# npm run build
source env/bin/activate
python manage.py collectstatic --noinput
# Bundle up an archive file
tar -cf kodjaz.tar authentication/ config/ courses/ fixtures/ frontend/ staticfiles/ server_configs/ requirements/ users/ manage.py robots.txt .env
# Load variables form .env file
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
    tar -xf kodjaz.tar

    sed -i 's/DEBUG=True/DEBUG=False/' .env

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

    source env/bin/activate && echo 'Activated env' || echo $SERVER_PASS sudo -S apt install python3.8-venv --yes && python3 -m venv env && source env/bin/activate && echo 'Installed venv and activated env';
    echo "Now installing python packages"
    pip install --upgrade pip
    pip install -r requirements/requirements_prod.txt
    echo "Applying migrations"
    python manage.py migrate --noinput --settings=config.settings_prod
    echo "Exiting"
    exit
END
