import csv
from csv import DictReader

from pymongo import MongoClient

'''
Part 1: connection to the database
'''

# connection with the local server on the port 27017 (default)
client = MongoClient('localhost', 27017)

# connection with the database (created already in mongodb)
cinema_db = client['cinema']

'''
Part 2: Creation of schema by using a validator & creation of the collection
'''

# validator.
# Mandatory fiels: title, year and director. The rest is optional.
# Changed the order of information.
movies_validator = {
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["title", "year", "director"],
    "properties": {
      "title": {
        "bsonType": "string",
        "description": "must be a string and is required"
      },
      "year": {
        "bsonType": "int",
        "description": "must be an integer and is required"
      },
      "director": {
        "bsonType": "string",
        "description": "must be a string and is required"
      },
       "cast": {
        "bsonType": "string",
        "description": "must be a string if provided"
      },
      "summary": {
        "bsonType": "string",
        "description": "must be a string if provided"
      },
      "short_summary": {
        "bsonType": "string",
        "description": "must be a string if provided"
      },
      "imdb_id": {
        "bsonType": "string",
        "description": "must be a string if provided"
      },
      "runtime": {
        "bsonType": "string",
        "description": "must be a string if provided"
      },
      "youtube_trailer": {
        "bsonType": "string",
        "description": "must be a string if provided"
      },
      "rating": {
        "bsonType": "string",
        "description": "must be a string if provided"
      },
      "movie_poster": {
        "bsonType": "string",
        "description": "must be a string if provided"
      },
      "writers": {
        "bsonType": "string",
        "description": "must be a string if provided"
      }
    }
  }
}


# creation of the collection
cinema_db.create_collection("movies", validator=movies_validator)

# connection with the collection
movies_coll = cinema_db["movies"]

'''
Part 3: importing csv file from local
'''

# defining the file path
csv_path = r"C:\Users\filip\OneDrive\Pulpit\Diginamic\27 - MongoDB avec Python\movies.csv"

# creating a mapping function
'''
Maps the CSV row fields to the corresponding MongoDB schema fields.
It also casts the year filed to integer.
'''

def map_csv(row):
    return {
        'title': row.get('Title'),
        'year': int(row.get('Year', 0)),
        'director': row.get('Director'),
        'cast': row.get('Cast', ''),
        'summary': row.get('Summary', ''),
        'short_summary': row.get('Short Summary', ''),
        'imdb_id': row.get('IMDB ID', ''),
        'runtime': row.get('Runtime', ''),
        'youtube_trailer': row.get('YouTube Trailer', ''),
        'rating': row.get('Rating', ''),
        'movie_poster': row.get('Movie Poster', ''),
        'writers': row.get('Writers', '')
    }

# opening the file in the read mode, encoding utf-8
with open(csv_path, "r", encoding="utf-8") as csvfile:
    movies_data = DictReader(csvfile)

    # converrting each row of data into a dictionary
    for row in movies_data:
        mapped_row = map_csv(row)
        movies_coll.insert_one(mapped_row)

if movies_coll.count_documents({}) != 0:
    print("Movies have successfully been added to the database")



