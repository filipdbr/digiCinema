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
#Movie.add_movie_by_user()

# Lister les 5 réalisateurs les mieux notés
# Comment: I gave the user an option to choose a number of directors they want to see
Director.top_rating(5)

# Les 5 réalisateurs dont les films ont la durée moyenne la plus importante
# Comment: Again I gave a user an option to choose
Director.top_avg_lenght(5)

# Les 5 réalisateurs ayant le plus de films
# Comment: Again I gave a user an option to choose
Director.top_number_of_movies(5)

# Requête d'agrégation : Le résultat de cette requête doit me donner la liste et le nombre de films
# des 15 acteurs le splus présents (avec leurs films,cf screenshot ci-dessus)
Movie.top_number_of_films(15)

