import os
from flask import Flask, render_template, request, jsonify
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

@app.route('/')
def index():
    return render_template('movies.html')

@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies = list(movies_collection.find({}, {"title": 1, "year": 1, "genres": 1, "plot": 1}))
    for m in movies:
        m["_id"] = str(m["_id"])
        m["title"] = m.get("title", "")
        m["year"] = m.get("year", "")
        m["genres"] = m.get("genres", [])
        m["plot"] = m.get("plot", "")
    return jsonify(movies)

@app.route('/api/movies', methods=['POST'])
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

@app.route('/api/movies/<id>', methods=['PUT'])
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
    movie["_id"] = str(movie["_id"])
    return jsonify(movie)

@app.route('/api/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    movies_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"result": "success"})

if __name__ == '__main__':
    app.run(debug=True) 