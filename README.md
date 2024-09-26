# **MongoDB and PyMongo Application**

## **Overview**
This project is the final assignment for a Python and MongoDB course at Diginamic (26/09/2024). The application manages movie and director data using MongoDB with the PyMongo library, implementing key functionalities like data import, CRUD operations, and aggregation queries.

---

## **How to Set Up the Project**

### **1. Clone the Repository**

```bash
git clone <repository-url>
cd <repository-directory>
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Set Up Your Data**

Ensure your MongoDB service is running locally on port `27017`.

To import your own CSV data, set the path to your `CSV file` in the `csv_path` variable in the `load_data.py` module **(line 127)**:

```python
csv_path = r"your_local_csv_path.csv"
```

## Project Structure

 - `load_data.py`: Handles the import of movie data from a CSV file to MongoDB. 
 - `director.py` and `movie.py`: Contain the classes for Director and Movie objects, including methods for adding new instances and interacting with MongoDB.
 - `main.py`: The main entry point for interacting with the project, such as querying movies, listing directors, and performing aggregations.

## Core Functionalities

1. **Data Import**: Imports movie data from a CSV file into the movies collection in MongoDB.
2. **Directors and Movies**: Ensures that directors and movies are added via classes that manage the integrity of the data.
3. **Aggregation Queries**: Lists top directors and performs movie-related queries (e.g., top-rated movies, movies with the longest runtime).
4. **Duplicate Protection**: Duplicate movie entries are not allowed.

## Info About the Data

### Pre-Cleaning
- **Duplicates Removed**: Movies with the same title but different directors are treated as distinct entities.
- **Whitespace Cleaned**: Leading and trailing whitespaces are removed from data entries.

### Normalization

- **Formatting**: Titles and director names are consistently capitalized.
- **Data Types**: Data types are standardized across all records.

### Note:

 `year = 0` means no year was provided during data entry.
 
### What Hasn't Been Done

- A common class for both Director and Movie to manage the _id property and a generic get_by_id method.
- Externalizing the MongoDB connection into a singleton.