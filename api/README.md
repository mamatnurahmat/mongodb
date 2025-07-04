# Movie REST API

API ini menyediakan endpoint CRUD untuk resource movie menggunakan Flask dan MongoDB.

## Persyaratan
- Python 3.x
- MongoDB
- Dependensi Python:
  - Flask
  - Flask-PyMongo
  - python-dotenv
  - bson

## Instalasi Dependensi

```bash
pip install -r requirements.txt
```

## Konfigurasi
Buat file `.env` dan tambahkan variabel berikut:

```
MONGO_URI=mongodb://localhost:27017
```

Ganti URI sesuai konfigurasi MongoDB Anda.

## Menjalankan API

```bash
python api.py
```

API akan berjalan di port 8000.

## Endpoint

### 1. GET /v1/movie
Ambil semua data movie atau lakukan pencarian berdasarkan title, year, dan genre.

**Request:**
```
GET http://localhost:8000/v1/movie
GET http://localhost:8000/v1/movie?title=Inception
GET http://localhost:8000/v1/movie?year=2010
GET http://localhost:8000/v1/movie?genre=Action
GET http://localhost:8000/v1/movie?title=Inception&year=2010&genre=Action
```

**Contoh dengan curl:**
```bash
# Ambil semua movie
curl -X GET http://localhost:8000/v1/movie

# Cari berdasarkan title
curl -X GET "http://localhost:8000/v1/movie?title=Inception"

# Cari berdasarkan year
curl -X GET "http://localhost:8000/v1/movie?year=2010"

# Cari berdasarkan genre
curl -X GET "http://localhost:8000/v1/movie?genre=Action"

# Cari kombinasi title, year, dan genre
curl -X GET "http://localhost:8000/v1/movie?title=Inception&year=2010&genre=Action"
```

**Response:**
```json
[
  {
    "_id": "...",
    "title": "Inception",
    "year": 2010,
    "genres": ["Action", "Sci-Fi"],
    "plot": "A thief who steals corporate secrets..."
  },
  ...
]
```

Jika year bukan angka:
```json
{
  "error": "Year must be an integer"
}
```

---

### 1a. GET /v1/movie/<id>
Ambil data movie berdasarkan ID.

**Request:**
```
GET http://localhost:8000/v1/movie/ID_MOVIE
```

**Contoh dengan curl:**
```bash
curl -X GET http://localhost:8000/v1/movie/ID_MOVIE
```

**Response:**
```json
{
  "_id": "...",
  "title": "Inception",
  "year": 2010,
  "genres": ["Action", "Sci-Fi"],
  "plot": "A thief who steals corporate secrets..."
}
```

Jika ID tidak ditemukan:
```json
{
  "error": "Movie not found"
}
```

---

### 2. POST /v1/movie
Tambah data movie baru.

**Request:**
```
POST http://localhost:8000/v1/movie
Content-Type: application/json

{
  "title": "Inception",
  "year": 2010,
  "genres": ["Action", "Sci-Fi"],
  "plot": "A thief who steals corporate secrets..."
}
```

**Contoh dengan curl:**
```bash
curl -X POST http://localhost:8000/v1/movie \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Inception",
    "year": 2010,
    "genres": ["Action", "Sci-Fi"],
    "plot": "A thief who steals corporate secrets..."
  }'
```

**Response:**
```json
{
  "_id": "...",
  "title": "Inception",
  "year": 2010,
  "genres": ["Action", "Sci-Fi"],
  "plot": "A thief who steals corporate secrets..."
}
```

---

### 3. PUT /v1/movie/<id>
Update data movie berdasarkan ID.

**Request:**
```
PUT http://localhost:8000/v1/movie/ID_MOVIE
Content-Type: application/json

{
  "title": "Inception Updated"
}
```

**Contoh dengan curl:**
```bash
curl -X PUT http://localhost:8000/v1/movie/ID_MOVIE \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Inception Updated"
  }'
```

**Response:**
```json
{
  "_id": "...",
  "title": "Inception Updated",
  "year": 2010,
  "genres": ["Action", "Sci-Fi"],
  "plot": "A thief who steals corporate secrets..."
}
```

---

### 4. DELETE /v1/movie/<id>
Hapus data movie berdasarkan ID.

**Request:**
```
DELETE http://localhost:8000/v1/movie/ID_MOVIE
```

**Contoh dengan curl:**
```bash
curl -X DELETE http://localhost:8000/v1/movie/ID_MOVIE
```

**Response:**
```json
{
  "result": "success"
}
```

---

## Catatan
- Pastikan MongoDB berjalan dan database `sample_mflix` beserta koleksi `movies` tersedia.
- Semua response dalam format JSON. 