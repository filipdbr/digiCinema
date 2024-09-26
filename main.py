from database_connection import directors_coll
from models.director import Director

test = Director("Tarantino", {"Kill Bill 1", "kill bill 2", "pulp fiction"})
test.save_to_db()
print(test.get_movies())
