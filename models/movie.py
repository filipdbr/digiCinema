from dataclasses import dataclass


@dataclass
class Movie:
    title: str
    year: int
    director: str
    cast: str
    summary: str
    short_summary: str
    imdb_id: str
    runtime: int
    youtube_trailer: str
    rating: float
    movie_poster: str
    writers: str