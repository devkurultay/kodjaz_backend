#!/bin/bash
tar -cf codomodo.tar config/ courses/ server_configs/ static/ requirements/ users/ manage.py requirements.txt
scp codomodo.tar almaz@104.248.142.48:lessons/
rm  codomodo.tar
ssh -tt almaz@104.248.142.48 << END
    cd lessons/
    tar -xf codomodo.tar

    source env/bin/activate
    pip install -r requirements/requirements_prod.txt
    pip install --upgrade pip
    python manage.py migrate --noinput --settings=config.settings_prod
    python manage.py collectstatic --noinput
    exit
END
