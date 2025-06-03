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
    Recette_id INTEGER,
    Id_ingredient INTEGER,
    Valeur INTEGER,
    Unite TEXT,
    FOREIGN KEY (Recette_id) REFERENCES Recettes(Recette_id),
    FOREIGN KEY (Id_ingredient) REFERENCES Ingredients(Id_ingredient)
);

CREATE TABLE Equipment (
    Id_equipement INTEGER PRIMARY KEY,
    Name TEXT,
    Recette_id INTEGER,
    FOREIGN KEY (Recette_id) REFERENCES Recettes(Recette_id)
);

CREATE TABLE Rating (
    User_id INTEGER,
    Recette_id INTEGER,
    Rating INTEGER,
    Commentaire TEXT,
    PRIMARY KEY (User_id, Recette_id),
    FOREIGN KEY (User_id) REFERENCES Users(User_id),
    FOREIGN KEY (Recette_id) REFERENCES Recettes(Recette_id)
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

# Réouvre la connexion
conn = sqlite3.connect("BDD.db")
cursor = conn.cursor()

# Insère la recette
cursor.execute("""
INSERT INTO Recettes (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (1, "Salade fraîcheur à la pastèque, feta et menthe", 15, 0, "Entrée", "Été",
      "Une salade légère et rafraîchissante, parfaite pour les journées chaudes.", 4, "salade_pasteque.jpg"))

# Étapes de préparation
steps = [
    "Coupez la pastèque en cubes.",
    "Émiettez la feta et ciselez la menthe.",
    "Mélangez tous les ingrédients dans un saladier.",
    "Arrosez d’un filet d’huile d’olive et ajoutez une pincée de sel.",
    "Servez bien frais."
]
for i, contenu in enumerate(steps, start=1):
    cursor.execute("""
    INSERT INTO Steps (Recette_id, Num_step, Contenu)
    VALUES (?, ?, ?)
    """, (1, i, contenu))

# Ingrédients (ajoute-les s'ils n'existent pas déjà)
ingredients = [
    (1, "Pastèque", False),
    (2, "Feta", True),
    (3, "Menthe", False),
    (4, "Huile d'olive", False),
    (5, "Sel", False)
]
for ing in ingredients:
    cursor.execute("INSERT INTO Ingredients (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)", ing)

# Quantités pour la recette (table Quantity)
quantities = [
    (1, 1, 500, "grammes"),
    (1, 2, 150, "grammes"),
    (1, 3, 10, "feuilles"),
    (1, 4, 2, "cuillères à soupe"),
    (1, 5, 1, "pincée")
]
for q in quantities:
    cursor.execute("""
    INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
    VALUES (?, ?, ?, ?)
    """, q)

# Matériel (Equipment) lié à la recette 1
equipments = [
    (1, "Saladier", 1),
    (2, "Couteau", 1),
    (3, "Cuillère", 1)
]
for eq in equipments:
    cursor.execute("INSERT INTO Equipment (Id_equipement, Name, Recette_id) VALUES (?, ?, ?)", eq)

# Exemple d'ajout d'une note (Rating)
cursor.execute("""
INSERT INTO Rating (User_id, Recette_id, Rating, Commentaire)
VALUES (?, ?, ?, ?)
""", (1, 1, 5, "Délicieux et rafraîchissant !"))

# Sauvegarde et fermeture
conn.commit()
conn.close()