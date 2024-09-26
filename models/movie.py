from dataclasses import dataclass, field
from multiprocessing.util import is_exiting
from typing import Optional

from database_connection import movies_coll


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

    def to_dict(self) -> dict:
        """Converts the Movie instance to a dictionary, excluding None values."""
        return {key: value for key, value in {
            "title": self.title,
            "year": self.year,
            "director": self.director,
            "cast": self.cast,
            "summary": self.summary,
            "short_summary": self.short_summary,
            "imdb_id": self.imdb_id,
            "runtime": self.runtime,
            "youtube_trailer": self.youtube_trailer,
            "rating": self.rating,
            "movie_poster": self.movie_poster,
            "writers": self.writers
        }.items() if value is not None}

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

    # Function to interact with the user and add a movie with optional data
    @staticmethod
    def add_movie_by_user():
        try:
            # Get mandatory data
            movie_title = input("\nEnter the movie title: ").strip().title()
            director_name = input("Enter the director's name: ").strip().title()
            year = input("Enter the release year: ").strip()

            # Validate that the mandatory fields are provided
            if not director_name or not movie_title or not year:
                raise ValueError("The director's name, movie title, and year must be provided.")

            # Convert year to int
            year = int(year)

        except ValueError as ve:
            print(f"Input error: {ve}")
            return

        # Optional data input
        cast = input("Enter the cast (optional): ").strip().title() or None
        summary = input("Enter the summary (optional): ").strip().capitalize() or None
        short_summary = input("Enter the short summary (optional): ").strip().capitalize() or None
        imdb_id = input("Enter the IMDb ID (optional): ").strip() or None
        runtime = input("Enter the runtime in minutes (optional): ").strip()
        runtime = int(runtime) if runtime else None
        rating = input("Enter the rating (optional, 0.0 - 10.0): ").strip()
        rating = float(rating) if rating else None
        youtube_trailer = input("Enter the YouTube trailer URL (optional): ").strip() or None
        movie_poster = input("Enter the movie poster URL (optional): ").strip() or None
        writers = input("Enter the writers (optional): ").strip().title() or None

        # Create the movie object
        try:
            movie = Movie(
                title=movie_title,
                year=year,
                director=director_name,
                cast=cast,
                summary=summary,
                short_summary=short_summary,
                imdb_id=imdb_id,
                runtime=runtime,
                rating=rating,
                youtube_trailer=youtube_trailer,
                movie_poster=movie_poster,
                writers=writers
            )
        except ValueError as ve:
            print(f"Error creating movie: {ve}")
            return

        movie_exists = bool(movies_coll.find_one({'title': movie.title}))

        # Save to database (or update if it exists)
        movies_coll.update_one(
            {'title': movie.title, 'director': movie.director, 'year': movie.year},
            {'$set': movie.to_dict()},
            upsert=True
        )

        if movie_exists:
            print(f"Movie '{movie.title}' by {movie.director} has been updated in the database.")
        else:
            print(f"Movie '{movie.title}' by {movie.director} has been added in the database.")


