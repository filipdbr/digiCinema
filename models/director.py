from dataclasses import dataclass, field
from typing import Set

@dataclass
class Director:
    """Represents a film director with a name and a set of movies they have directed."""

    name: str
    movies: Set[str] = field(default_factory=set)

    def __post_init__(self):
        #Validates the director's name after initialization
        self.name = self._validate_name(self.name)

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
