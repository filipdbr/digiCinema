from pymongo import MongoClient


'''
First module to run
This module is responsible for daily connection to the database
'''
# connection with the local server on the port 27017 (default)
client = MongoClient('localhost', 27017)

# connection with the database (created already in mongodb)
cinema_db = client['cinema']

# connection with the collections
movies_coll = cinema_db["movies"]
directors_coll = cinema_db["directors"]

# Function initailizing the collections in case they don't exist
def initialize_collections():
    if 'movies' not in cinema_db.list_collection_names():
        cinema_db.create_collection('movies')
    if 'directors' not in cinema_db.list_collection_names():
        cinema_db.create_collection('directors')

    # indexes creation
    movies_coll.create_index([("title", 1), ("imdb_id", 1)], unique=True)
    directors_coll.create_index("name", unique=True)

# initializing collections
initialize_collections()

print("The connection with the database has been established")



