import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flasgger import Swagger, swag_from

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

# Konfigurasi Swagger
app.config['SWAGGER'] = {
    'title': 'Movie API',
    'uiversion': 3
}
swagger = Swagger(app)

mongo = PyMongo(app)

# Gunakan database sample_mflix dan collection movies
movies_collection = mongo.cx["sample_mflix"]["movies"]

@app.route('/v1/movie', methods=['GET'])
@swag_from({
    'tags': ['Movie'],
    'parameters': [
        {
            'name': 'title',
            'in': 'query',
            'type': 'string',
            'description': 'Cari berdasarkan judul',
        },
        {
            'name': 'year',
            'in': 'query',
            'type': 'integer',
            'description': 'Cari berdasarkan tahun',
        },
        {
            'name': 'genre',
            'in': 'query',
            'type': 'string',
            'description': 'Cari berdasarkan genre',
        }
    ],
    'responses': {
        200: {
            'description': 'Daftar movie',
            'examples': {
                'application/json': [
                    {
                        '_id': 'string',
                        'title': 'string',
                        'year': 2020,
                        'genres': ['Action'],
                        'plot': 'string'
                    }
                ]
            }
        }
    }
})
def get_movies():
    query = {}
    title = request.args.get('title')
    year = request.args.get('year')
    genre = request.args.get('genre')
    if title:
        query['title'] = {'$regex': title, '$options': 'i'}
    if year:
        try:
            query['year'] = int(year)
        except ValueError:
            return jsonify({"error": "Year must be an integer"}), 400
    if genre:
        query['genres'] = genre
    movies = list(movies_collection.find(query, {"title": 1, "year": 1, "genres": 1, "plot": 1}))
    for m in movies:
        m["_id"] = str(m["_id"])
        m["title"] = m.get("title", "")
        m["year"] = m.get("year", "")
        m["genres"] = m.get("genres", [])
        m["plot"] = m.get("plot", "")
    return jsonify(movies)

@app.route('/v1/movie', methods=['POST'])
@swag_from({
    'tags': ['Movie'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'year': {'type': 'integer'},
                    'genres': {'type': 'array', 'items': {'type': 'string'}},
                    'plot': {'type': 'string'}
                },
                'required': ['title', 'year']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Movie berhasil dibuat',
            'examples': {
                'application/json': {
                    '_id': 'string',
                    'title': 'string',
                    'year': 2020,
                    'genres': ['Action'],
                    'plot': 'string'
                }
            }
        },
        400: {
            'description': 'Input tidak valid'
        }
    }
})
def create_movie():
    data = request.json
    title = data.get('title')
    year = data.get('year')
    genres = data.get('genres', [])
    plot = data.get('plot', '')
    if not title or not year:
        return jsonify({"error": "Title and year are required"}), 400
    movie = {
        "title": title,
        "year": int(year),
        "genres": genres,
        "plot": plot
    }
    result = movies_collection.insert_one(movie)
    movie["_id"] = str(result.inserted_id)
    return jsonify(movie), 201

@app.route('/v1/movie/<id>', methods=['GET'])
@swag_from({
    'tags': ['Movie'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID movie'
        }
    ],
    'responses': {
        200: {
            'description': 'Detail movie',
            'examples': {
                'application/json': {
                    '_id': 'string',
                    'title': 'string',
                    'year': 2020,
                    'genres': ['Action'],
                    'plot': 'string'
                }
            }
        },
        404: {
            'description': 'Movie tidak ditemukan'
        }
    }
})
def get_movie_by_id(id):
    movie = movies_collection.find_one({"_id": ObjectId(id)}, {"title": 1, "year": 1, "genres": 1, "plot": 1})
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    movie["_id"] = str(movie["_id"])
    return jsonify(movie)

@app.route('/v1/movie/<id>', methods=['PUT'])
@swag_from({
    'tags': ['Movie'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID movie'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'year': {'type': 'integer'},
                    'genres': {'type': 'array', 'items': {'type': 'string'}},
                    'plot': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Movie berhasil diupdate',
            'examples': {
                'application/json': {
                    '_id': 'string',
                    'title': 'string',
                    'year': 2020,
                    'genres': ['Action'],
                    'plot': 'string'
                }
            }
        },
        400: {
            'description': 'Input tidak valid'
        },
        404: {
            'description': 'Movie tidak ditemukan'
        }
    }
})
def update_movie(id):
    data = request.json
    update_fields = {}
    for field in ["title", "year", "genres", "plot"]:
        if field in data:
            update_fields[field] = data[field]
    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400
    if "year" in update_fields:
        update_fields["year"] = int(update_fields["year"])
    movies_collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
    movie = movies_collection.find_one({"_id": ObjectId(id)}, {"title": 1, "year": 1, "genres": 1, "plot": 1})
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    movie["_id"] = str(movie["_id"])
    return jsonify(movie)

@app.route('/v1/movie/<id>', methods=['DELETE'])
@swag_from({
    'tags': ['Movie'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID movie'
        }
    ],
    'responses': {
        200: {
            'description': 'Movie berhasil dihapus',
            'examples': {
                'application/json': {
                    'result': 'success'
                }
            }
        },
        404: {
            'description': 'Movie tidak ditemukan'
        }
    }
})
def delete_movie(id):
    result = movies_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify({"result": "success"})

@app.route('/v2/movie', methods=['GET'])
@swag_from({
    'tags': ['Movie'],
    'parameters': [
        {'name': 'title', 'in': 'query', 'type': 'string', 'description': 'Cari berdasarkan judul'},
        {'name': 'year', 'in': 'query', 'type': 'integer', 'description': 'Cari berdasarkan tahun'},
        {'name': 'genre', 'in': 'query', 'type': 'string', 'description': 'Cari berdasarkan genre'},
        {'name': 'limit', 'in': 'query', 'type': 'integer', 'description': 'Jumlah data per halaman', 'default': 10},
        {'name': 'page', 'in': 'query', 'type': 'integer', 'description': 'Halaman ke-', 'default': 1}
    ],
    'responses': {
        200: {
            'description': 'Daftar movie dengan pagination',
            'examples': {
                'application/json': {
                    'data': [
                        {
                            '_id': 'string',
                            'title': 'string',
                            'year': 2020,
                            'genres': ['Action'],
                            'plot': 'string'
                        }
                    ],
                    'total': 100,
                    'page': 1,
                    'limit': 10,
                    'total_pages': 10
                }
            }
        }
    }
})
def get_movies_v2():
    query = {}
    title = request.args.get('title')
    year = request.args.get('year')
    genre = request.args.get('genre')
    limit = request.args.get('limit', default=10, type=int)
    page = request.args.get('page', default=1, type=int)
    if title:
        query['title'] = {'$regex': title, '$options': 'i'}
    if year:
        try:
            query['year'] = int(year)
        except ValueError:
            return jsonify({"error": "Year must be an integer"}), 400
    if genre:
        query['genres'] = genre
    total = movies_collection.count_documents(query)
    total_pages = (total + limit - 1) // limit if limit > 0 else 1
    skip = (page - 1) * limit if page > 0 else 0
    cursor = movies_collection.find(query, {"title": 1, "year": 1, "genres": 1, "plot": 1}).skip(skip).limit(limit)
    data = []
    for m in cursor:
        m["_id"] = str(m["_id"])
        m["title"] = m.get("title", "")
        m["year"] = m.get("year", "")
        m["genres"] = m.get("genres", [])
        m["plot"] = m.get("plot", "")
        data.append(m)
    return jsonify({
        "data": data,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 