#!/bin/bash

echo "Setting up PostgreSQL"
echo "====================="
echo

echo "Getting local IP..."
LOCAL_IP=$(ifconfig tunl0 | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*')
echo "Local IP is $LOCAL_IP"
export LOCAL_IP=${LOCAL_IP}
echo

echo
echo "Searching for PostgreSQL configuration file..."
POSTGRES_CONF_FILE=$(locate postgresql.conf | head -n 1)
echo "PostgreSQL configuration file is ${POSTGRES_CONF_FILE}"
echo

echo "Adding local IP into the PostgreSQL configuration..."
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost,$LOCAL_IP'/g" "$POSTGRES_CONF_FILE"
echo

echo "Searching for PostgreSQL Host Based Authentication file..."
HBA_FILE=$(locate pg_hba.conf | head -n 1)
echo "PostgreSQL Host Based Authentication file is $HBA_FILE"
echo

HBA_RECORD="host    all             all             172.17.0.0/8            md5"
HBA_RECORD_EXIST=$(sudo cat "$HBA_FILE" | grep "$HBA_RECORD")

if [ -z "$HBA_RECORD_EXIST" ] ; then
  echo "Adding new record into $HBA_FILE"
  echo "$HBA_RECORD" | sudo tee -a "$HBA_FILE"
  echo
fi

echo
echo "Restarting PostgreSQL..."
service postgresql restart

LAB_NAME="lab1_db"
echo
echo "Creating the Database..."
su -c "psql -c 'CREATE DATABASE $LAB_NAME'" - postgres

USER_NAME="postgres"
USER_PASSWORD="evraz2021"
echo
echo "Setting password for db user $USER_NAME"
su -c "psql -d $LAB_NAME -c \"ALTER USER $USER_NAME PASSWORD '$USER_PASSWORD';\"" - postgres

echo
echo "Adding new records to the database"
su -c "psql -d $LAB_NAME -c \"CREATE TABLE IF NOT EXISTS $LAB_NAME(\"id\" SERIAL PRIMARY KEY, \"name\" varchar(100), \"bdate\" date);\"" - postgres
su -c "psql -d $LAB_NAME -c \"INSERT INTO $LAB_NAME (name, bdate) VALUES ('ERIC CLAPTON', '1945-03-30'::date);\"" - postgres
su -c "psql -d $LAB_NAME -c \"INSERT INTO $LAB_NAME (name, bdate) VALUES ('TOM PETTY', '1950-10-20'::date);\"" - postgres
su -c "psql -d $LAB_NAME -c \"INSERT INTO $LAB_NAME (name, bdate) VALUES ('GEORGE HARRISON', '1943-02-25'::date);\"" - postgres
su -c "psql -d $LAB_NAME -c \"INSERT INTO $LAB_NAME (name, bdate) VALUES ('BOB DYLAN', '1941-05-24'::date);\"" - postgres
su -c "psql -d $LAB_NAME -c \"INSERT INTO $LAB_NAME (name, bdate) VALUES ('ROY KELTON', '1936-04-23'::date);\"" - postgres

echo
echo "Reading the table content..."
su -c "psql -d $LAB_NAME -c \"SELECT * FROM $LAB_NAME\"" - postgres
