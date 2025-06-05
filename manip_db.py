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
    Name TEXT UNIQUE,
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
    Name TEXT UNIQUE
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
                     
CREATE TABLE Recette_Equipment (
    Recette_id INTEGER,
    Id_equipement INTEGER,
    PRIMARY KEY (Recette_id, Id_equipement),
    FOREIGN KEY (Recette_id) REFERENCES Recettes(Recette_id),
    FOREIGN KEY (Id_equipement) REFERENCES Equipment(Id_equipement)
);

""")

# AJOUT DESSERTS ETE
import sqlite3

conn = sqlite3.connect("BDD.db")
cursor = conn.cursor()

# Ingrédients communs (ajoutés une seule fois)
ingredients = [
    ("Fraises", 0),
    ("Pêches", 0),
    ("Abricots", 0),
    ("Pastèque", 0),
    ("Myrtilles", 0),
    ("Sucre", 0),
    ("Crème fraîche", 1),
    ("Yaourt", 1),
    ("Menthe", 0),
    ("Citron", 0)
]
for name, allergene in ingredients:
    cursor.execute("INSERT OR IGNORE INTO Ingredients (Name, Allergene) VALUES (?, ?)", (name, allergene))

# Équipements communs
equipments = ["Saladier", "Couteau", "Cuillère", "Mixeur", "Verres"]
for equip in equipments:
    cursor.execute("INSERT OR IGNORE INTO Equipment (Name) VALUES (?)", (equip,))

# Recettes d'été
desserts = [
    {
        "title": "Salade de fraises à la menthe",
        "fruits": [("Fraises", 250, "g")],
        "autres": [("Sucre", 30, "g"), ("Menthe", 5, "feuilles"), ("Citron", 1, "pcs")],
        "equip": ["Saladier", "Couteau", "Cuillère"],
        "steps": [
            "Laver et couper les fraises.",
            "Ciseler la menthe.",
            "Mélanger fraises, sucre, menthe et jus de citron dans un saladier.",
            "Servir frais."
        ]
    },
    {
        "title": "Smoothie pêche-abricot",
        "fruits": [("Pêches", 2, "pcs"), ("Abricots", 3, "pcs")],
        "autres": [("Yaourt", 1, "pot"), ("Sucre", 20, "g")],
        "equip": ["Mixeur", "Verres", "Couteau"],
        "steps": [
            "Laver, dénoyauter et couper les fruits.",
            "Mettre les fruits, le yaourt et le sucre dans le mixeur.",
            "Mixer jusqu'à consistance lisse.",
            "Verser dans des verres et servir frais."
        ]
    },
    {
        "title": "Pastèque glacée",
        "fruits": [("Pastèque", 400, "g")],
        "autres": [("Menthe", 5, "feuilles")],
        "equip": ["Couteau", "Saladier"],
        "steps": [
            "Couper la pastèque en cubes.",
            "Ciseler la menthe.",
            "Mélanger et placer au congélateur 30 minutes.",
            "Servir très frais."
        ]
    },
    {
        "title": "Abricots rôtis au yaourt",
        "fruits": [("Abricots", 4, "pcs")],
        "autres": [("Yaourt", 1, "pot"), ("Sucre", 15, "g")],
        "equip": ["Saladier", "Cuillère"],
        "steps": [
            "Couper les abricots en deux et les saupoudrer de sucre.",
            "Les faire rôtir au four 10 minutes.",
            "Servir avec du yaourt."
        ]
    },
    {
        "title": "Myrtilles à la crème",
        "fruits": [("Myrtilles", 150, "g")],
        "autres": [("Crème fraîche", 50, "g"), ("Sucre", 10, "g")],
        "equip": ["Saladier", "Cuillère"],
        "steps": [
            "Mélanger les myrtilles avec la crème et le sucre.",
            "Servir frais."
        ]
    }
]

for idx, dessert in enumerate(desserts, start=1):
    # Ajout recette
    cursor.execute("""
        INSERT INTO Recettes (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        idx,
        dessert["title"],
        10,  # Preptime
        0,   # Cooktime
        "Dessert",
        "Été",
        dessert["title"],
        4,
        ""
    ))

    # Ajout étapes
    for num, step in enumerate(dessert["steps"], start=1):
        cursor.execute("""
            INSERT INTO Steps (Recette_id, Num_step, Contenu)
            VALUES (?, ?, ?)
        """, (idx, num, step))

    # Ajout ingrédients et quantités
    for name, valeur, unite in dessert["fruits"] + dessert["autres"]:
        cursor.execute("SELECT Id_ingredient FROM Ingredients WHERE Name = ?", (name,))
        id_ing = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
            VALUES (?, ?, ?, ?)
        """, (idx, id_ing, valeur, unite))

    # Ajout équipements
    for equip in dessert["equip"]:
        cursor.execute("SELECT Id_equipement FROM Equipment WHERE Name = ?", (equip,))
        id_equip = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO Recette_Equipment (Recette_id, Id_equipement)
            VALUES (?, ?)
        """, (idx, id_equip))


# Sauvegarde les changements et ferme la connexion
conn.commit()
conn.close()