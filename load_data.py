from tqdm import tqdm
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

# Create a composite index on title and imdb_id, ensuring unique combinations
# it is necessary as there are some movies with the same title, which are not duplicates
movies_coll.create_index([("title", 1), ("imdb_id", 1)], unique=True)

'''
Part 3: importing csv file from local + data cleaning and normalization
'''

# defining the file path
csv_path = r"C:\Users\filip\OneDrive\Pulpit\Diginamic\27 - MongoDB avec Python\movies.csv"

# creating a mapping function
'''
Maps the CSV row fields to the corresponding MongoDB schema fields.

Data normalization and data cleaning:
    - casts the year
    - trims the white space
    - provides consistent formatting, such as capitalizing the title and director names
'''

def map_csv(row):
    return {
        'title': row.get('Title', '').strip().title(),  # Normalizing title to lowercase
        'year': int(row.get('Year', 0)),
        'director': row.get('Director', '').strip().title(),
        'cast': row.get('Cast', '').strip().title(),
        'summary': row.get('Summary', '').strip().capitalize(),
        'short_summary': row.get('Short Summary', '').strip().capitalize(),
        'imdb_id': row.get('IMDB ID', '').strip(),
        'runtime': row.get('Runtime', '').strip(),
        'youtube_trailer': row.get('YouTube Trailer', '').strip(),
        'rating': row.get('Rating', '').strip(),
        'movie_poster': row.get('Movie Poster', '').strip(),
        'writers': row.get('Writers', '').strip().title()
    }

'''
Imports the csv file to the databas

Data cleaning: duplicates removal
'''

# creating the set to keep the duplicated movies
movies_to_add = set()

# opening the file in the read mode, encoding utf-8
with open(csv_path, "r", encoding="utf-8") as csvfile:
    movies_data = DictReader(csvfile)

    # converting each row of data into a dictionary
    # added tqdm to add some visual effects to the app
    for row in tqdm(movies_data, desc="Importing movies", unit=" movies"):
        mapped_row = map_csv(row)

        # creation of the key
        movie_key = (mapped_row['imdb_id'], mapped_row['title'])

        if movie_key in movies_to_add:
            print(f"The duplicate found: {mapped_row['title']}, id imdb: {mapped_row['imdb_id']}")
        else:
            movies_coll.insert_one(mapped_row)
            movies_to_add.add(movie_key)


# final message informing of the result
if movies_coll.count_documents({}) != 0:
    print("Movies have successfully been added to the database")
elif movies_coll.count_documents({}) == 0:
    print("No movies has been added to the database")



