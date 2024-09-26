from dataclasses import dataclass, field, asdict
from typing import Set

from database_connection import directors_coll


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

    def get_movies(self) -> Set[str]:
        """
        Retrieves the set of movies directed by the director.
        """
        return self.movies

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
        directors_coll.update_one(
            {'name': self.name},
            {'$addToSet': {'movies': {'$each': director_dict['movies']}}},
            upsert=True
        )
        return print(f"Director {self.name} has been saved to database.")




