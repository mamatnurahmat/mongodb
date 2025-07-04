import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# Gunakan database sample_mflix dan collection movies
movies_collection = mongo.cx["sample_mflix"]["movies"]

@app.route('/v1/movie', methods=['GET'])
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
def get_movie_by_id(id):
    movie = movies_collection.find_one({"_id": ObjectId(id)}, {"title": 1, "year": 1, "genres": 1, "plot": 1})
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    movie["_id"] = str(movie["_id"])
    return jsonify(movie)

@app.route('/v1/movie/<id>', methods=['PUT'])
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
def delete_movie(id):
    result = movies_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify({"result": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 