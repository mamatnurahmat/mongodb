#!/bin/bash

# Konfigurasi
JSON_FILE="sample_mflix.movies.json"
DB_NAME="mflix"
COLLECTION="movie"
USER="mflix_rw"
PASSWORD="rw_password"
MONGO_IMAGE="mongo:4.4"

if [ ! -f "$JSON_FILE" ]; then
  echo "File $JSON_FILE tidak ditemukan!"
  exit 1
fi

# # Deteksi host untuk docker (Linux vs Mac/Windows)
# LOCAL_HOST="localhost"
# if [[ "$OSTYPE" == "darwin"* ]] || grep -q Microsoft /proc/version 2>/dev/null; then
#   LOCAL_HOST="host.docker.internal"
# fi
LOCAL_HOST=192.168.11.12
# Import data

echo "Mengimpor $JSON_FILE ke $DB_NAME.$COLLECTION ..."
docker run --rm -v "$PWD:/import" $MONGO_IMAGE \
  mongoimport --uri="mongodb://$USER:$PASSWORD@$LOCAL_HOST:27017/$DB_NAME" \
  --collection=$COLLECTION --file="/import/$JSON_FILE" --jsonArray

if [ $? -eq 0 ]; then
  echo "Import selesai!"
else
  echo "Import gagal!"
  exit 2
fi 