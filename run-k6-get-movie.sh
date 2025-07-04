#!/bin/bash

# Jalankan k6 load test
k6 run k6-get-movie.js --out json=report.json

# Install k6-reporter jika belum ada
type k6-reporter >/dev/null 2>&1 || npm install -g k6-reporter

# Convert report ke HTML
echo "Membuat report HTML..."
k6-reporter report.json

echo "Report HTML tersimpan di summary.html" 