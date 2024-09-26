from aggregation.list_of_films import save_directors_movies
from models.director import Director
from models.movie import Movie

# inserting David Lynch data as it's my favourite director. 5 random movies
lynch = Director("David Lynch", {"Blue Velvet", "Mulholland Drive", "Twin Peaks", "The Elephant Man"})

# saving into db
lynch.save_to_db()

# TP: Enregistrer dans une nouvelle collection (ou vue, comme vous voulez) la liste des réalisateurs avec la liste de leurs films
# test
directors = ["christopher nolan", "Quentin Tarantino"]
save_directors_movies(directors, output_collection='tarantino_nolan')

# TP: Implémenter la méthode permettant de lister les films d'un réalisateur
# test
lynch.get_movies()

# Implémenter la méthode permettant de connaitre la note moyenne d'un réalisateur (dans sa classe)
lynch.get_avg_rating()

# Implémenter la méthode d'ajout de film par interaction utilisateur
Movie.add_movie_by_user()

