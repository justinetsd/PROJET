import sqlite3

# Crée la base SQLite
conn = sqlite3.connect("BDD.db")
cursor = conn.cursor()

# Supprime les anciennes tables si elles existent
tables = [
    "Users", "Recettes", "Steps", "Ingredients", "Quantity", "Equipment", "Rating",
    "Recette_Ingredients", "Recette_Equipment", "Recette_Favoris", "User_Recette_Rating"
]
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Crée les tables
cursor.executescript("""
CREATE TABLE Users (
    User_id INTEGER PRIMARY KEY,
    Username TEXT,
    FirstName TEXT,
    LastName TEXT,
    EmailAddress TEXT,
    Sign_in_date TEXT,
    Salt TEXT,
    Random TEXT,
    Hash TEXT
);

CREATE TABLE Recettes (
    Recette_id INTEGER PRIMARY KEY,
    Title TEXT,
    Preptime INTEGER,
    Cooktime INTEGER,
    Category TEXT,
    Saison TEXT,
    Description TEXT,
    Servings INTEGER,
    Image TEXT
);

CREATE TABLE Steps (
    Recette_id INTEGER,
    Num_step INTEGER,
    Contenu TEXT,
    PRIMARY KEY (Recette_id, Num_step),
    FOREIGN KEY (Recette_id) REFERENCES Recettes(Recette_id)
);

CREATE TABLE Ingredients (
    Id_ingredient INTEGER PRIMARY KEY,
    Name TEXT,
    Allergene BOOLEAN
);

CREATE TABLE Quantity (
    Valeur INTEGER,
    Unite TEXT
);

CREATE TABLE Recette_Ingredients (
    Recette_id INTEGER,
    Id_ingredient INTEGER,
    Valeur INTEGER,
    Unite TEXT,
    FOREIGN KEY (Recette_id) REFERENCES Recettes(Recette_id),
    FOREIGN KEY (Id_ingredient) REFERENCES Ingredients(Id_ingredient)
);

CREATE TABLE Equipment (
    Id_equipement INTEGER PRIMARY KEY,
    Name TEXT
);

CREATE TABLE Recette_Equipment (
    Recette_id INTEGER,
    Id_equipement INTEGER,
    FOREIGN KEY (Recette_id) REFERENCES Recettes(Recette_id),
    FOREIGN KEY (Id_equipement) REFERENCES Equipment(Id_equipement)
);

CREATE TABLE Rating (
    Rating_id INTEGER PRIMARY KEY,
    Rating INTEGER,
    Commentaire TEXT
);

CREATE TABLE User_Recette_Rating (
    User_id INTEGER,
    Recette_id INTEGER,
    Rating_id INTEGER,
    FOREIGN KEY (User_id) REFERENCES Users(User_id),
    FOREIGN KEY (Recette_id) REFERENCES Recettes(Recette_id),
    FOREIGN KEY (Rating_id) REFERENCES Rating(Rating_id)
);

CREATE TABLE Recette_Favoris (
    User_id INTEGER,
    Recette_id INTEGER,
    FOREIGN KEY (User_id) REFERENCES Users(User_id),
    FOREIGN KEY (Recette_id) REFERENCES Recettes(Recette_id)
);
""")

# Sauvegarde et ferme la connexion
conn.commit()
conn.close()