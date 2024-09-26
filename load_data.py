from pymongo.errors import CollectionInvalid, OperationFailure
from tqdm import tqdm
from csv import DictReader

from database_connection import cinema_db, directors_coll, movies_coll

'''
This module initializes the dababases and creates collections for the first time 

Part 1: Creation of schema by validators and update of databases
'''

# Movies validator
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
        "bsonType": "int",
        "description": "must be a string if provided"
      },
      "youtube_trailer": {
        "bsonType": "string",
        "description": "must be a string if provided"
      },
      "rating": {
        "bsonType": "float",
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

# Director validator
director_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "director name: must be a string and is required"
            },
            "movies" : {
                "bsonType": "array",
                "items": {
                    "bsonType": "string",
                },
                "description": "list of movies directed by the director: must be a string if provided"
            }
        }
    }
}

# Function which will be used in create_collections. It modifies the current validator.
def create_or_update_collection(collection_name, validator):
    try:
        # Try to create the collection with the validator
        cinema_db.create_collection(collection_name, validator=validator)
    except CollectionInvalid:
        # If collection exists, update its validator
        try:
            cinema_db.command({
                'collMod': collection_name,
                'validator': validator
            })
        except OperationFailure as e:
            print(f"Failed to update validator for collection '{collection_name}': {str(e)}")

# creation of collections
def create_collections():
    # Create or update the movies collection with its validator
    create_or_update_collection("movies", movies_validator)

    # Create or update the directors collection with its validator
    create_or_update_collection("directors", director_validator)

    # Create indexes after collection creation or update
    # Ensure that the unique constraints are enforced
    movies_coll.create_index([("title", 1), ("imdb_id", 1)], unique=True)
    directors_coll.create_index("name", unique=True)

'''
Part 2: importing csv file from local + data cleaning and normalization
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
def map_csv_movie(row):
    return {
        'title': row.get('Title', '').strip().title(),  # Normalizing title to lowercase
        'year': int(row.get('Year', 0)),
        'director': row.get('Director', '').strip().title(),
        'cast': row.get('Cast', '').strip().title(),
        'summary': row.get('Summary', '').strip().capitalize(),
        'short_summary': row.get('Short Summary', '').strip().capitalize(),
        'imdb_id': row.get('IMDB ID', '').strip(),
        'runtime': int(row.get('Runtime', '').strip()),
        'youtube_trailer': row.get('YouTube Trailer', '').strip(),
        'rating': float(row.get('Rating', '').strip()),
        'movie_poster': row.get('Movie Poster', '').strip(),
        'writers': row.get('Writers', '').strip().title()
    }

'''
Imports the csv file to the database

Data cleaning: duplicates removal
'''

# creating the set to keep the duplicated movies
movies_to_add = set()

if __name__ == "__main__":

    create_collections()

    # opening the file in the read mode, encoding utf-8
    with open(csv_path, "r", encoding="utf-8") as csvfile:
        movies_data = DictReader(csvfile)

        # converting each row of data into a dictionary
        # added tqdm to add some visual effects to the app
        for row in tqdm(movies_data, desc="Importing movies data", unit=" movies"):
            mapped_row = map_csv_movie(row)

            # creation of the key
            movie_key = (mapped_row['imdb_id'], mapped_row['title'])

            if movie_key in movies_to_add:
                print(f"The duplicate found: {mapped_row['title']}, id imdb: {mapped_row['imdb_id']}")
            else:
                movies_coll.insert_one(mapped_row)
                movies_to_add.add(movie_key)

                director_name = mapped_row['director']
                movie = mapped_row['title']

                directors_coll.update_one(
                    {"name": director_name},
                    {"$addToSet": {"movies": movie}},
                    upsert=True
                )


    # final message informing of the result
    if movies_coll.count_documents({}) != 0:
        print(f"New records have been added to the database:\n"
              f"{movies_coll.count_documents({})} movies\n"
              f"{directors_coll.count_documents({})} directors ")
    elif movies_coll.count_documents({}) == 0:
        print("No movies has been added to the database")



