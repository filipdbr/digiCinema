from dataclasses import dataclass, field
from typing import Optional


# todo: consider classmethod / factory beam
@dataclass
class Movie:
    """Represents a movie"""

    title: str
    year: int
    director: str
    cast: Optional[str] = field(default=None)
    summary: Optional[str] = field(default=None)
    short_summary: Optional[str] = field(default=None)
    imdb_id: Optional[str] = field(default=None)
    runtime: Optional[int] = field(default=None)
    youtube_trailer: Optional[str] = field(default=None)
    rating: Optional[float] = field(default=None)
    movie_poster: Optional[str] = field(default=None)
    writers: Optional[str] = field(default=None)

    def __post_init__(self):
        """
        Validates mandatory data (title, director, year) and additional data as runtime and rating.
        Also provides consistent text formatting.
        """
        self.title = self._validate_title(self.title)
        self.director = self._validate_director(self.director)
        self.year = self._validate_year(self.year)
        if self.runtime:
            self.runtime = self._validate_runtime(self.runtime)
        if self.rating:
            self.rating = self._validate_rating(self.rating)

    def _validate_title(self, title: str) -> str:
        """
        Validates and formats the movie title.
        """
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string.")
        return title.strip().title()

    def _validate_director(self, director: str) -> str:
        """
        Validates and formats the director's name.
        """
        if not director or not isinstance(director, str):
            raise ValueError("Director must be a non-empty string.")
        return director.strip().title()

    def _validate_year(self, year: int) -> int:
        """
        Validates the year the movie was released.
        """
        if not isinstance(year, int) or year < 1900:  # The first movie was made in 1888.
            raise ValueError("Year must be a valid integer representing the release year.")
        return year


    def _validate_runtime(self, runtime: int) -> int:
        """
        Validates the runtime of the movie. Can't be shorter than 0 minutes.
        """
        if not isinstance(runtime, int) or runtime <= 0:
            raise ValueError("Runtime must be a positive integer representing the number of minutes.")
        return runtime

    def _validate_rating(self, rating: float) -> float:
        """
        Validates the movie rating. Must be between 0 and 10.
        """
        if not isinstance(rating, (float, int)) or not (0.0 <= rating <= 10.0):
            raise ValueError("Rating must be a float between 0.0 and 10.0.")
        return rating

    """
    Validates and formats the title.
    """
    def to_dict(self) -> dict:
        """
        Converts the Movie instance to a dictionary.
        """
        movie_dict = self.to_dict()
        return movie_dict

    def update_summary(self, new_summary: str):
        """
        Updates the summary of the movie.
        """
        if not new_summary or not isinstance(new_summary, str):
            raise ValueError("Summary must be a non-empty string.")
        self.summary = new_summary.strip().capitalize()

    def is_classic(self) -> bool:
        """
        Returns True if the movie is more than 25 years old.
        """
        from datetime import datetime
        current_year = datetime.now().year
        return current_year - self.year > 25

    def add_writer(self, writer: str):
        """
        Adds a new writer to the movie's writers.
        """
        if not writer or not isinstance(writer, str):
            raise ValueError("Writer name must be a non-empty string.")
        self.writers += f", {writer.strip().title()}"

    def __str__(self):
        """
        Returns a string representation of the Movie instance.
        """
        return (
            f"Title: {self.title}\n"
            f"Year: {self.year}\n"
            f"Director: {self.director}\n"
            f"Cast: {self.cast}\n"
            f"Summary: {self.summary}\n"
            f"Short Summary: {self.short_summary}\n"
            f"IMDb ID: {self.imdb_id}\n"
            f"Runtime: {self.runtime} minutes\n"
            f"Rating: {self.rating}/10\n"
            f"YouTube Trailer: {self.youtube_trailer}\n"
            f"Movie Poster: {self.movie_poster}\n"
            f"Writers: {self.writers}\n"
        )


