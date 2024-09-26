from database_connection import movies_coll, directors_coll

"""
The module contains 2 functions letting looking for a list of movies of:
1. many directors: first function
2. one director: second function
"""

# Enregistrer dans une nouvelle collection (ou vue, comme vous voulez) la liste des réalisateurs avec la liste de leurs films
def save_directors_movies(director_names, output_collection:str = 'directors_with_movies'):
    """
    Aggregates movies by the given list of directors and saves the result to a new collection.
    """

    # in order that the search is not case-sensitive
    regex_conditions = [{'director': {'$regex': name, '$options': 'i'}} for name in director_names]

    pipeline = [
        {'$match': {'$or': regex_conditions}},
        {
            '$group': {
                '_id': '$director',
                'movies': {'$addToSet': '$title'}
            }
        },
        {
            '$project': {
                '_id': 0,
                'name': '$_id',
                'movies': 1
            }
        },
        {
            '$out': output_collection  # Output to the specified collection
        }
    ]

    # Execute the aggregation pipeline
    movies_coll.aggregate(pipeline)

    print(f"The list of directors and movies was added to '{output_collection}' collection.")

