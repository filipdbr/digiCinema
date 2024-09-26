from dataclasses import dataclass, field, asdict
from typing import Set

from database_connection import directors_coll, movies_coll


# todo: consider classmethod / factory beam
@dataclass
class Director:
    """Represents a film director with a name and a set of movies they have directed."""

    name: str
    movies: Set[str] = field(default_factory=set)

    def __post_init__(self):
        #Validates the director's name after initialization
        self.name = self._validate_name(self.name)
        self.movies = {movie.strip().title() for movie in self.movies} # changing formatting of text to title()

    def _validate_name(self, name: str) -> str:
        """
        Validates and formats the director's name.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string consisting of letters")
        if len(name) < 3 or len(name) > 50:
            raise ValueError("Name must be between 3 and 50 characters")
        return name.strip().title()

    def add_movie(self, movie: str):
        """
        Adds a movie title to the director's set of movies.
        """
        if not movie or not isinstance(movie, str):
            raise ValueError("Movie title must be a non-empty string")
        self.movies.add(movie.strip().title())

    def to_dict(self) -> dict:
        """
        Changes director instance to a dictionary.
        """
        director_dict = asdict(self)
        director_dict['movies'] = list(director_dict['movies'])
        return director_dict

    def save_to_db(self):
        """
        Saves the director to the *directors* database.
        """
        director_dict = self.to_dict()
        result = directors_coll.update_one(
            {'name': self.name},
            {'$addToSet': {'movies': {'$each': director_dict['movies']}}},
            upsert=True
        )
        if result.modified_count > 0:
            return print(f"Data regarding {self.name} has been updated.")

        return print(f"Director {self.name} has been saved to database.")

    # funtion listing average rating of a director
    def get_avg_rating(self):

        pipeline = [
            {
                '$match': {
                    'director': self.name
                }
            }, {
                '$group': {
                    '_id': '$director',
                    'avg_rating': {
                        '$avg': '$rating'
                    }
                }
            }
        ]

        result = list(movies_coll.aggregate(pipeline))

        # Print the result if it's not empty
        if result:
            # Access the first (and likely only) result
            first_result = result[0]
            print(f"The average rating of {first_result['_id']} is {first_result['avg_rating']}")
        else:
            print(f"No data found for director: {self.name}")

    # Implémenter la méthode permettant de lister les films d'un réalisateur (dans sa classe)
    def get_movies(self):

        pipeline = [

            {'$match': {'name': self.name}
             },
            {
                '$project': {
                    '_id': '$name',
                    'movies': 1  # Include the movies array as is
                }
            }
        ]

        # Execute the aggregation
        result = directors_coll.aggregate(pipeline)

        # Print the result in the desired format
        for director in result:
            print(f"Movies directed by {director['_id']}:")
            for movie in director['movies']:
                print(f"- {movie}")



