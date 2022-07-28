#!/bin/bash
source .env
ssh -tt $SERVER_USERNAME@$SERVER_IP << END
  sudo apt install python3-dev libpq-dev postgresql postgresql-contrib python3-psycopg2 --yes
  sudo -u postgres psql
  CREATE DATABASE $DB_NAME;
  CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
  ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
  ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
  ALTER ROLE $DB_USER SET timezone TO 'Asia/Bishkek';
  GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
  \q
  exit;
END
