#!/bin/bash

# Konfigurasi
REMOTE_URI="mongodb+srv://devops:pwlpi123@cluster0.xvw7kcr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
LOCAL_URI="mongodb://admin_user:admin_password@localhost:27017/admin"
DUMP_DIR="$(pwd)/dump_atlas"
MONGO_IMAGE="mongo:4.4"

# Fungsi untuk menjalankan mongodump
run_mongodump() {
    if command -v mongodump &> /dev/null; then
        mongodump --uri="$REMOTE_URI" --out="$DUMP_DIR"
    else
        echo "mongodump tidak ditemukan, menggunakan docker..."
        docker run --rm -v "$DUMP_DIR:/dump" "$MONGO_IMAGE" \
            mongodump --uri="$REMOTE_URI" --out=/dump
    fi
}

# Fungsi untuk menjalankan mongorestore
run_mongorestore() {
    if command -v mongorestore &> /dev/null; then
        mongorestore --uri="$LOCAL_URI" "$DUMP_DIR"
    else
        echo "mongorestore tidak ditemukan, menggunakan docker..."
        # host.docker.internal untuk Mac/Windows, localhost untuk Linux
        LOCAL_HOST="localhost"
        if [[ "$OSTYPE" == "darwin"* ]] || grep -q Microsoft /proc/version 2>/dev/null; then
            LOCAL_HOST="host.docker.internal"
        fi
        docker run --rm -v "$DUMP_DIR:/dump" "$MONGO_IMAGE" \
            mongorestore --uri="mongodb://admin_user:admin_password@$LOCAL_HOST:27017/admin" /dump
    fi
}

# 1. Dump dari Atlas
echo "[1/3] Melakukan mongodump dari Atlas..."
run_mongodump
if [ $? -ne 0 ]; then
    echo "Gagal melakukan mongodump dari Atlas."
    exit 2
fi

# 2. Restore ke lokal
echo "[2/3] Melakukan mongorestore ke MongoDB lokal..."
run_mongorestore
if [ $? -ne 0 ]; then
    echo "Gagal melakukan mongorestore ke lokal."
    exit 3
fi

echo "[3/3] Migrasi selesai!" 