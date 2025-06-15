import sqlite3, random

# Crée la base SQLite
conn = sqlite3.connect("BDD.db")
cursor = conn.cursor()

# Supprime les anciennes tables si elles existent
tables = [
    "User", "Recette", "Step", "Ingredient", "Quantity", "Equipment", "Rating", "Recette_Equipment", "Recette_Favori"
]
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Crée les tables
cursor.executescript("""
CREATE TABLE User (
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

CREATE TABLE Recette (
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

CREATE TABLE Step (
    Recette_id INTEGER,
    Num_step INTEGER,
    Contenu TEXT,
    PRIMARY KEY (Recette_id, Num_step),
    FOREIGN KEY (Recette_id) REFERENCES Recette(Recette_id)
);

CREATE TABLE Ingredient (
    Id_ingredient INTEGER PRIMARY KEY,
    Name TEXT UNIQUE,
    Allergene BOOLEAN
);

CREATE TABLE Quantity (
    Recette_id INTEGER,
    Id_ingredient INTEGER,
    Valeur INTEGER,
    Unite TEXT,
    FOREIGN KEY (Recette_id) REFERENCES Recette(Recette_id),
    FOREIGN KEY (Id_ingredient) REFERENCES Ingredient(Id_ingredient)
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
    FOREIGN KEY (User_id) REFERENCES User(User_id),
    FOREIGN KEY (Recette_id) REFERENCES Recette(Recette_id)
);

CREATE TABLE Recette_Favori (
    User_id INTEGER,
    Recette_id INTEGER,
    FOREIGN KEY (User_id) REFERENCES User(User_id),
    FOREIGN KEY (Recette_id) REFERENCES Recette(Recette_id)
);
                              
CREATE TABLE Recette_Equipment (
    Recette_id INTEGER,
    Id_equipement INTEGER,
    PRIMARY KEY (Recette_id, Id_equipement),
    FOREIGN KEY (Recette_id) REFERENCES Recette(Recette_id),
    FOREIGN KEY (Id_equipement) REFERENCES Equipment(Id_equipement)
);

""")

### AJOUT DES RECETTES --------------------------------------------------------------------------------------------------------------

# AJOUT DESSERTS ETE

# Ingrédients communs (ajoutés une seule fois)
ingredients = [
    "Fraises", "Pêches", "Abricots", "Pastèque", "Myrtilles", "Sucre",
    "Crème fraîche", "Yaourt", "Menthe", "Citron"
]
allergenes = {
    "Crème fraîche": 1,
    "Yaourt": 1
}

# Générer des identifiants uniques à 5 chiffres pour chaque ingrédient
ingredient_ids = {}
used_ing_ids = set()
for name in ingredients:
    while True:
        new_id = random.randint(10000, 99999)
        if new_id not in used_ing_ids:
            used_ing_ids.add(new_id)
            ingredient_ids[name] = new_id
            break
    cursor.execute(
        "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
        (ingredient_ids[name], name, allergenes.get(name, 0))
    )

# Équipements communs
equipments = ["Saladier", "Couteau", "Cuillère", "Mixeur", "Verres"]
equipment_ids = {}
used_equip_ids = set()
for equip in equipments:
    while True:
        new_id = random.randint(10000, 99999)
        if new_id not in used_equip_ids:
            used_equip_ids.add(new_id)
            equipment_ids[equip] = new_id
            break
    cursor.execute(
        "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
        (equipment_ids[equip], equip)
    )

# Recettes d'été
desserts = [
    {
        "title": "Salade de fraises à la menthe",
        "description": "Une salade fraîche et légère alliant fraises sucrées et menthe parfumée.",
        "fruits": [("Fraises", 250, "g")],
        "autres": [("Sucre", 30, "g"), ("Menthe", 5, "feuilles"), ("Citron", 1, "pcs")],
        "equip": ["Saladier", "Couteau", "Cuillère"],
        "steps": [
            "Laver et couper les fraises.",
            "Ciseler la menthe.",
            "Mélanger fraises, sucre, menthe et jus de citron dans un saladier.",
            "Servir frais."
        
        ],
        "image": "Salade de fraises à la menthe.jpg"
    },
    {
        "title": "Smoothie pêche-abricot",
        "description": "Un smoothie fruité et onctueux, parfait pour une pause vitaminée.",
        "fruits": [("Pêches", 2, "pcs"), ("Abricots", 3, "pcs")],
        "autres": [("Yaourt", 1, "pot"), ("Sucre", 20, "g")],
        "equip": ["Mixeur", "Verres", "Couteau"],
        "steps": [
            "Laver, dénoyauter et couper les fruits.",
            "Mettre les fruits, le yaourt et le sucre dans le mixeur.",
            "Mixer jusqu'à consistance lisse.",
            "Verser dans des verres et servir frais."
        ],
        "image": "Smoothie pêche-abricot.jpg"
    },
    {
        "title": "Pastèque glacée",
        "description": "Une douceur glacée et rafraîchissante à base de pastèque et de menthe.",
        "fruits": [("Pastèque", 400, "g")],
        "autres": [("Menthe", 5, "feuilles")],
        "equip": ["Couteau", "Saladier"],
        "steps": [
            "Couper la pastèque en cubes.",
            "Ciseler la menthe.",
            "Mélanger et placer au congélateur 30 minutes.",
            "Servir très frais."
        ],
        
        "image": "Pastèque glacée.jpg"
    },
    {
        "title": "Abricots rôtis au yaourt",
        "description": "Des abricots caramélisés au four, servis avec une touche de yaourt frais.",
        "fruits": [("Abricots", 4, "pcs")],
        "autres": [("Yaourt", 1, "pot"), ("Sucre", 15, "g")],
        "equip": ["Saladier", "Cuillère"],
        "steps": [
            "Couper les abricots en deux et les saupoudrer de sucre.",
            "Les faire rôtir au four 10 minutes.",
            "Servir avec du yaourt."
        ],
        "image": "Abricots rôtis au yaourt.jpg"
    },
    {
        "title": "Myrtilles à la crème",
        "description": "Un dessert simple et gourmand mêlant myrtilles fraîches et crème sucrée.",
        "fruits": [("Myrtilles", 150, "g")],
        "autres": [("Crème fraîche", 50, "g"), ("Sucre", 10, "g")],
        "equip": ["Saladier", "Cuillère"],
        "steps": [
            "Mélanger les myrtilles avec la crème et le sucre.",
            "Servir frais."
        ],
        "image": "Myrtilles à la crème.jpg"
    }
]

# Générer des identifiants uniques à 5 chiffres pour chaque dessert
used_ids = set()
while len(used_ids) < len(desserts):
    new_id = random.randint(10000, 99999)
    used_ids.add(new_id)
dessert_ids = list(used_ids)

for idx, dessert in enumerate(desserts):
    recette_id = dessert_ids[idx]

    # Ajout recette
    cursor.execute("""
        INSERT INTO Recette (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recette_id,
        dessert["title"],
        10,  # Preptime
        0,   # Cooktime
        "Dessert",
        "Été",
        dessert["description"],
        4,
        dessert["image"]
        
    ))

    # Ajout étapes
    for num, step in enumerate(dessert["steps"], start=1):
        cursor.execute("""
            INSERT INTO Step (Recette_id, Num_step, Contenu)
            VALUES (?, ?, ?)
        """, (recette_id, num, step))

    # Ajout ingrédients et quantités
    for name, valeur, unite in dessert["fruits"] + dessert["autres"]:
        id_ing = ingredient_ids[name]
        cursor.execute("""
            INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
            VALUES (?, ?, ?, ?)
        """, (recette_id, id_ing, valeur, unite))

    # Ajout équipements
    for equip in dessert["equip"]:
        id_equip = equipment_ids[equip]
        cursor.execute("""
            INSERT INTO Recette_Equipment (Recette_id, Id_equipement)
            VALUES (?, ?)
        """, (recette_id, id_equip))

# DESSERTS AUTOMNE

ingredients_automne = [
    "Pommes", "Poires", "Noix", "Châtaignes", "Raisins", "Farine", "Beurre", "Sucre", "Oeufs", "Cannelle", "Crème fraîche"
]
allergenes_automne = {
    "Crème fraîche": 1,
    "Oeufs": 1,
    "Noix": 1,
    "Farine": 1,
    "Beurre": 1
}

# Ajoute les nouveaux ingrédients d'automne avec gestion des allergènes
for name in ingredients_automne:
    if name not in ingredient_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_ing_ids:
                used_ing_ids.add(new_id)
                ingredient_ids[name] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
            (ingredient_ids[name], name, allergenes_automne.get(name, 0))
        )

equipments_automne = ["Saladier", "Couteau", "Four", "Poêle", "Moule à tarte", "Mixeur"]
for equip in equipments_automne:
    if equip not in equipment_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_equip_ids:
                used_equip_ids.add(new_id)
                equipment_ids[equip] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
            (equipment_ids[equip], equip)
        )

desserts_automne = [
    {
        "title": "Tarte aux pommes et noix",
        "description": "Tarte rustique garnie de pommes fondantes et de noix croquantes.",
        "fruits": [("Pommes", 3, "pcs")],
        "autres": [("Noix", 50, "g"), ("Farine", 200, "g"), ("Beurre", 100, "g"), ("Sucre", 80, "g"), ("Oeufs", 2, "pcs")],
        "equip": ["Moule à tarte", "Saladier", "Four", "Couteau"],
        "steps": [
            "Préparez la pâte avec farine, beurre, sucre et œufs.",
            "Étalez la pâte dans un moule à tarte.",
            "Disposez les pommes tranchées et parsemez de noix.",
            "Saupoudrez de sucre.",
            "Faites cuire au four 35 minutes à 180°C."
        ],
        "image": "Tarte aux pommes et noix.jpg"
    },
    {
        "title": "Poêlée de poires aux raisins et noix",
        "description": "Poires poêlées avec raisins secs et éclats de noix, parfumées à la cannelle.",
        "fruits": [("Poires", 2, "pcs"), ("Raisins", 40, "g")],
        "autres": [("Noix", 30, "g"), ("Beurre", 20, "g"), ("Sucre", 20, "g"), ("Cannelle", 1, "c. à café")],
        "equip": ["Poêle", "Couteau"],
        "steps": [
            "Épluchez et coupez les poires en quartiers.",
            "Faites fondre le beurre dans une poêle.",
            "Ajoutez les poires, raisins, noix et sucre.",
            "Saupoudrez de cannelle et faites revenir 10 minutes.",
            "Servez tiède."
        ],
        "image": "Poêlée de poires aux raisins et noix.jpg"
    },
    {
        "title": "Moelleux aux châtaignes",
        "description": "Gâteau moelleux à la farine de châtaigne et éclats de marrons.",
        "fruits": [("Châtaignes", 100, "g")],
        "autres": [("Farine", 120, "g"), ("Beurre", 80, "g"), ("Sucre", 80, "g"), ("Oeufs", 3, "pcs")],
        "equip": ["Saladier", "Four", "Mixeur"],
        "steps": [
            "Mixez les châtaignes en purée.",
            "Mélangez avec farine, sucre, œufs et beurre fondu.",
            "Versez dans un moule beurré.",
            "Faites cuire 30 minutes à 180°C.",
            "Laissez tiédir avant de démouler."
        ],
        "image": "Moelleux aux châtaignes.jpg"
    },
    {
        "title": "Pommes rôties à la crème",
        "description": "Pommes rôties au four, servies avec une crème fraîche sucrée.",
        "fruits": [("Pommes", 4, "pcs")],
        "autres": [("Sucre", 30, "g"), ("Crème fraîche", 80, "g")],
        "equip": ["Four", "Saladier", "Couteau"],
        "steps": [
            "Évidez les pommes et disposez-les dans un plat.",
            "Saupoudrez de sucre.",
            "Faites rôtir 25 minutes à 180°C.",
            "Servez avec la crème fraîche sucrée."
        ],
        "image": "Pommes rôties à la crème.jpg"
    },
    {
        "title": "Clafoutis aux raisins",
        "description": "Dessert fondant aux raisins frais dans une pâte à clafoutis.",
        "fruits": [("Raisins", 200, "g")],
        "autres": [("Farine", 100, "g"), ("Sucre", 60, "g"), ("Oeufs", 3, "pcs"), ("Beurre", 40, "g")],
        "equip": ["Four", "Saladier", "Moule à tarte"],
        "steps": [
            "Mélangez farine, sucre, œufs et beurre fondu.",
            "Ajoutez les raisins.",
            "Versez dans un moule beurré.",
            "Faites cuire 35 minutes à 180°C.",
            "Servez tiède ou froid."
        ],
        "image": "Clafoutis aux raisins.jpg"
    }
]

# Générer des identifiants uniques à 5 chiffres pour chaque dessert d'automne
used_ids_automne = set()
while len(used_ids_automne) < len(desserts_automne):
    new_id = random.randint(10000, 99999)
    if new_id not in used_ids and new_id not in used_ids_automne:
        used_ids_automne.add(new_id)
dessert_ids_automne = list(used_ids_automne)

for idx, dessert in enumerate(desserts_automne):
    recette_id = dessert_ids_automne[idx]

    # Ajout recette
    cursor.execute("""
        INSERT INTO Recette (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recette_id,
        dessert["title"],
        15,  # Preptime
        30,  # Cooktime
        "Dessert",
        "Automne",
        dessert["description"],
        4,
        dessert["image"]
    ))

    # Ajout étapes
    for num, step in enumerate(dessert["steps"], start=1):
        cursor.execute("""
            INSERT INTO Step (Recette_id, Num_step, Contenu)
            VALUES (?, ?, ?)
        """, (recette_id, num, step))

    # Ajout ingrédients et quantités
    for name, valeur, unite in dessert["fruits"] + dessert["autres"]:
        id_ing = ingredient_ids[name]
        cursor.execute("""
            INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
            VALUES (?, ?, ?, ?)
        """, (recette_id, id_ing, valeur, unite))

    # Ajout équipements
    for equip in dessert["equip"]:
        id_equip = equipment_ids[equip]
        cursor.execute("""
            INSERT INTO Recette_Equipment (Recette_id, Id_equipement)
            VALUES (?, ?)
        """, (recette_id, id_equip))

# DESSERTS HIVER

ingredients_hiver = [
    "Pommes", "Poires", "Orange", "Chocolat", "Noisettes", "Farine", "Beurre", "Sucre", "Oeufs", "Cannelle", "Crème fraîche", "Lait"
]
allergenes_hiver = {
    "Crème fraîche": 1,
    "Oeufs": 1,
    "Noisettes": 1,
    "Farine": 1,
    "Beurre": 1,
    "Lait": 1,
    "Chocolat": 1  # si tu veux considérer le chocolat comme allergène (lait)
}

# Ajoute les nouveaux ingrédients d'hiver avec gestion des allergènes
for name in ingredients_hiver:
    if name not in ingredient_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_ing_ids:
                used_ing_ids.add(new_id)
                ingredient_ids[name] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
            (ingredient_ids[name], name, allergenes_hiver.get(name, 0))
        )

equipments_hiver = ["Saladier", "Couteau", "Four", "Poêle", "Moule à cake", "Mixeur", "Casserole"]
for equip in equipments_hiver:
    if equip not in equipment_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_equip_ids:
                used_equip_ids.add(new_id)
                equipment_ids[equip] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
            (equipment_ids[equip], equip)
        )

desserts_hiver = [
    {
        "title": "Moelleux au chocolat",
        "description": "Gâteau fondant au chocolat, parfait pour les journées froides.",
        "fruits": [],
        "autres": [("Chocolat", 200, "g"), ("Beurre", 100, "g"), ("Sucre", 80, "g"), ("Farine", 50, "g"), ("Oeufs", 4, "pcs")],
        "equip": ["Moule à cake", "Four", "Saladier", "Casserole"],
        "steps": [
            "Faites fondre le chocolat et le beurre au bain-marie.",
            "Ajoutez le sucre, la farine puis les œufs un à un.",
            "Versez dans un moule beurré.",
            "Faites cuire 20 minutes à 180°C.",
            "Servez tiède."
        ],
        "image": "Moelleux au chocolat.jpg"
    },
    {
        "title": "Compote de pommes et poires à la cannelle",
        "description": "Compote maison réconfortante, parfumée à la cannelle.",
        "fruits": [("Pommes", 3, "pcs"), ("Poires", 2, "pcs")],
        "autres": [("Sucre", 40, "g"), ("Cannelle", 1, "c. à café")],
        "equip": ["Casserole", "Couteau", "Saladier"],
        "steps": [
            "Épluchez et coupez pommes et poires en morceaux.",
            "Mettez-les dans une casserole avec le sucre et la cannelle.",
            "Faites cuire à feu doux 25 minutes.",
            "Écrasez ou mixez selon la texture désirée.",
            "Servez tiède ou froid."
        ],
        "image": "Compote de pommes et poires à la cannelle.png"
    },
    {
        "title": "Crêpes à l'orange",
        "description": "Crêpes moelleuses servies avec un sirop d'orange.",
        "fruits": [("Orange", 2, "pcs")],
        "autres": [("Farine", 150, "g"), ("Oeufs", 2, "pcs"), ("Lait", 300, "ml"), ("Beurre", 30, "g"), ("Sucre", 30, "g")],
        "equip": ["Saladier", "Poêle", "Couteau"],
        "steps": [
            "Préparez la pâte à crêpes avec farine, œufs, lait, beurre fondu et sucre.",
            "Laissez reposer 30 minutes.",
            "Faites cuire les crêpes dans une poêle chaude.",
            "Préparez un sirop avec le jus d'orange et un peu de sucre.",
            "Servez les crêpes nappées de sirop d'orange."
        ],
        "image": "Crêpes à l'orange.jpg"
    },
    {
        "title": "Riz au lait à la cannelle",
        "description": "Dessert crémeux et doux, parfumé à la cannelle.",
        "fruits": [],
        "autres": [("Lait", 500, "ml"), ("Riz rond", 100, "g"), ("Sucre", 60, "g"), ("Cannelle", 1, "c. à café")],
        "equip": ["Casserole", "Saladier"],
        "steps": [
            "Faites chauffer le lait dans une casserole.",
            "Ajoutez le riz et laissez cuire à feu doux 30 minutes.",
            "Ajoutez le sucre et la cannelle en fin de cuisson.",
            "Versez dans un saladier.",
            "Servez tiède ou froid."
        ],
        "image": "Riz au lait à la cannelle.jpg"
    },
    {
        "title": "Gâteau noisettes et pommes",
        "description": "Gâteau moelleux aux noisettes et morceaux de pommes.",
        "fruits": [("Pommes", 2, "pcs")],
        "autres": [("Noisettes", 80, "g"), ("Farine", 120, "g"), ("Beurre", 80, "g"), ("Sucre", 80, "g"), ("Oeufs", 2, "pcs")],
        "equip": ["Moule à cake", "Four", "Saladier", "Couteau"],
        "steps": [
            "Mélangez farine, noisettes en poudre, sucre, œufs et beurre fondu.",
            "Ajoutez les pommes coupées en dés.",
            "Versez dans un moule beurré.",
            "Faites cuire 35 minutes à 180°C.",
            "Laissez tiédir avant de démouler."
        ],
        "image": "Gâteau noisettes et pommes.jpg"
    }
]

# Générer des identifiants uniques à 5 chiffres pour chaque dessert d'hiver
used_ids_hiver = set()
while len(used_ids_hiver) < len(desserts_hiver):
    new_id = random.randint(10000, 99999)
    if new_id not in used_ids and new_id not in used_ids_automne and new_id not in used_ids_hiver:
        used_ids_hiver.add(new_id)
dessert_ids_hiver = list(used_ids_hiver)

for idx, dessert in enumerate(desserts_hiver):
    recette_id = dessert_ids_hiver[idx]

    # Ajout recette
    cursor.execute("""
        INSERT INTO Recette (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recette_id,
        dessert["title"],
        15,  # Preptime
        30,  # Cooktime
        "Dessert",
        "Hiver",
        dessert["description"],
        4,
        dessert["image"]
    ))

    # Ajout étapes
    for num, step in enumerate(dessert["steps"], start=1):
        cursor.execute("""
            INSERT INTO Step (Recette_id, Num_step, Contenu)
            VALUES (?, ?, ?)
        """, (recette_id, num, step))

    # Ajout ingrédients et quantités
    for name, valeur, unite in dessert["fruits"] + dessert["autres"]:
        # Pour le riz au lait, ajoute l'ingrédient si besoin
        if name not in ingredient_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_ing_ids:
                    used_ing_ids.add(new_id)
                    ingredient_ids[name] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
                (ingredient_ids[name], name, 0)
            )
        id_ing = ingredient_ids[name]
        cursor.execute("""
            INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
            VALUES (?, ?, ?, ?)
        """, (recette_id, id_ing, valeur, unite))

    # Ajout équipements
    for equip in dessert["equip"]:
        if equip not in equipment_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_equip_ids:
                    used_equip_ids.add(new_id)
                    equipment_ids[equip] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
                (equipment_ids[equip], equip)
            )
        id_equip = equipment_ids[equip]
        cursor.execute("""
            INSERT INTO Recette_Equipment (Recette_id, Id_equipement)
            VALUES (?, ?)
        """, (recette_id, id_equip))

# DESSERTS PRINTEMPS

ingredients_printemps = [
    "Fraises", "Rhubarbe", "Citron", "Menthe", "Fromage blanc", "Sucre", "Farine", "Beurre", "Oeufs", "Lait", "Vanille"
]
allergenes_printemps = {
    "Fromage blanc": 1,
    "Oeufs": 1,
    "Farine": 1,
    "Beurre": 1,
    "Lait": 1
}

# Ajoute les nouveaux ingrédients de printemps avec gestion des allergènes
for name in ingredients_printemps:
    if name not in ingredient_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_ing_ids:
                used_ing_ids.add(new_id)
                ingredient_ids[name] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
            (ingredient_ids[name], name, allergenes_printemps.get(name, 0))
        )

equipments_printemps = ["Saladier", "Couteau", "Four", "Moule à cake", "Mixeur", "Casserole", "Moule à tarte"]
for equip in equipments_printemps:
    if equip not in equipment_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_equip_ids:
                used_equip_ids.add(new_id)
                equipment_ids[equip] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
            (equipment_ids[equip], equip)
        )

desserts_printemps = [
    {
        "title": "Tarte fraises-rhubarbe",
        "description": "Tarte acidulée et sucrée aux fraises et à la rhubarbe.",
        "fruits": [("Fraises", 200, "g"), ("Rhubarbe", 150, "g")],
        "autres": [("Farine", 200, "g"), ("Beurre", 100, "g"), ("Sucre", 80, "g"), ("Oeufs", 2, "pcs")],
        "equip": ["Moule à tarte", "Four", "Couteau", "Saladier"],
        "steps": [
            "Préparez la pâte avec farine, beurre, sucre et œufs.",
            "Étalez la pâte dans un moule à tarte.",
            "Disposez la rhubarbe en tronçons et les fraises coupées.",
            "Saupoudrez de sucre.",
            "Faites cuire au four 35 minutes à 180°C."
        ],
        "image": "Tarte fraises-rhubarbe.jpg"
    },
    {
        "title": "Clafoutis fraises-menthe",
        "description": "Clafoutis moelleux aux fraises fraîches et parfum de menthe.",
        "fruits": [("Fraises", 250, "g")],
        "autres": [("Farine", 100, "g"), ("Sucre", 60, "g"), ("Oeufs", 3, "pcs"), ("Lait", 200, "ml"), ("Menthe", 5, "feuilles")],
        "equip": ["Four", "Saladier", "Moule à cake"],
        "steps": [
            "Mélangez farine, sucre, œufs, lait et menthe ciselée.",
            "Ajoutez les fraises coupées.",
            "Versez dans un moule beurré.",
            "Faites cuire 30 minutes à 180°C.",
            "Servez tiède ou froid."
        ],
        "image": "Clafoutis fraises-menthe.jpg"
    },
    {
        "title": "Compote rhubarbe-vanille",
        "description": "Compote douce et parfumée à la rhubarbe et à la vanille.",
        "fruits": [("Rhubarbe", 300, "g")],
        "autres": [("Sucre", 60, "g"), ("Vanille", 1, "gousse")],
        "equip": ["Casserole", "Saladier", "Couteau"],
        "steps": [
            "Épluchez et coupez la rhubarbe en tronçons.",
            "Faites cuire avec le sucre et la vanille fendue.",
            "Laissez compoter 20 minutes à feu doux.",
            "Retirez la gousse de vanille.",
            "Servez frais."
        ],
        "image": "Compote rhubarbe-vanille.jpg"
    },
    {
        "title": "Verrines fromage blanc, fraises et citron",
        "description": "Verrines fraîches au fromage blanc, fraises et zeste de citron.",
        "fruits": [("Fraises", 150, "g"), ("Citron", 1, "pcs")],
        "autres": [("Fromage blanc", 200, "g"), ("Sucre", 30, "g")],
        "equip": ["Saladier", "Couteau"],
        "steps": [
            "Mélangez le fromage blanc avec le sucre et le zeste de citron.",
            "Coupez les fraises en morceaux.",
            "Alternez couches de fromage blanc et fraises dans des verrines.",
            "Terminez par un peu de zeste de citron.",
            "Servez bien frais."
        ],
        "image": "Verrines fromage blanc, fraises et citron.jpg"
    },
    {
        "title": "Gâteau moelleux citron-menthe",
        "description": "Gâteau léger et parfumé au citron et à la menthe.",
        "fruits": [("Citron", 2, "pcs")],
        "autres": [("Farine", 150, "g"), ("Beurre", 80, "g"), ("Sucre", 80, "g"), ("Oeufs", 2, "pcs"), ("Menthe", 5, "feuilles")],
        "equip": ["Four", "Saladier", "Moule à cake"],
        "steps": [
            "Mélangez farine, sucre, œufs, beurre fondu, jus et zeste de citron.",
            "Ajoutez la menthe ciselée.",
            "Versez dans un moule beurré.",
            "Faites cuire 30 minutes à 180°C.",
            "Laissez tiédir avant de démouler."
        ],
        "image": "Gâteau moelleux citron-menthe.jpg"
    }
]

# Générer des identifiants uniques à 5 chiffres pour chaque dessert de printemps
used_ids_printemps = set()
while len(used_ids_printemps) < len(desserts_printemps):
    new_id = random.randint(10000, 99999)
    if (new_id not in used_ids and
        new_id not in used_ids_automne and
        new_id not in used_ids_hiver and
        new_id not in used_ids_printemps):
        used_ids_printemps.add(new_id)
dessert_ids_printemps = list(used_ids_printemps)

for idx, dessert in enumerate(desserts_printemps):
    recette_id = dessert_ids_printemps[idx]

    # Ajout recette
    cursor.execute("""
        INSERT INTO Recette (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recette_id,
        dessert["title"],
        15,  # Preptime
        30,  # Cooktime
        "Dessert",
        "Printemps",
        dessert["description"],
        4,
        dessert["image"]
    ))

    # Ajout étapes
    for num, step in enumerate(dessert["steps"], start=1):
        cursor.execute("""
            INSERT INTO Step (Recette_id, Num_step, Contenu)
            VALUES (?, ?, ?)
        """, (recette_id, num, step))

    # Ajout ingrédients et quantités
    for name, valeur, unite in dessert["fruits"] + dessert["autres"]:
        if name not in ingredient_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_ing_ids:
                    used_ing_ids.add(new_id)
                    ingredient_ids[name] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
                (ingredient_ids[name], name, allergenes_printemps.get(name, 0))
            )
        id_ing = ingredient_ids[name]
        cursor.execute("""
            INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
            VALUES (?, ?, ?, ?)
        """, (recette_id, id_ing, valeur, unite))

    # Ajout équipements
    for equip in dessert["equip"]:
        if equip not in equipment_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_equip_ids:
                    used_equip_ids.add(new_id)
                    equipment_ids[equip] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
                (equipment_ids[equip], equip)
            )
        id_equip = equipment_ids[equip]
        cursor.execute("""
            INSERT INTO Recette_Equipment (Recette_id, Id_equipement)
            VALUES (?, ?)
        """, (recette_id, id_equip))

# PLATS ÉTÉ

ingredients_ete_plats = [
    "Tomates", "Concombre", "Poivron", "Oignon", "Olives noires", "Thon", "Œufs", "Pâtes", "Mozzarella", "Basilic",
    "Courgettes", "Aubergines", "Poulet", "Citron", "Ail", "Persil", "Riz", "Saumon", "Avocat", "Maïs", "Pain", "Laitue"
]
allergenes_ete_plats = {
    "Œufs": 1,
    "Mozzarella": 1,
    "Thon": 1,
    "Saumon": 1,
    "Pain": 1,
    "Pâtes": 1
}

# Ajoute les nouveaux ingrédients d'été plats avec gestion des allergènes
for name in ingredients_ete_plats:
    if name not in ingredient_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_ing_ids:
                used_ing_ids.add(new_id)
                ingredient_ids[name] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
            (ingredient_ids[name], name, allergenes_ete_plats.get(name, 0))
        )

equipments_ete_plats = [
    "Saladier", "Couteau", "Four", "Poêle", "Moule à tarte", "Mixeur", "Planche à découper", "Cuillère", "Plat à gratin", "Barbecue", "Bol"
]
for equip in equipments_ete_plats:
    if equip not in equipment_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_equip_ids:
                used_equip_ids.add(new_id)
                equipment_ids[equip] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
            (equipment_ids[equip], equip)
        )

plats_ete = [
    {
        "title": "Salade niçoise",
        "description": "Salade méditerranéenne composée de légumes frais, thon et œufs durs.",
        "ingredients": [("Tomates", 3, "pcs"), ("Concombre", 1, "pcs"), ("Poivron", 1, "pcs"), ("Oignon", 1, "pcs"),
                        ("Olives noires", 50, "g"), ("Thon", 1, "boîte"), ("Œufs", 2, "pcs")],
        "equip": ["Saladier", "Couteau", "Planche à découper"],
        "steps": [
            "Faites cuire les œufs durs et laissez-les refroidir.",
            "Coupez tomates, concombre, poivron et oignon en morceaux.",
            "Mélangez tous les légumes, ajoutez le thon émietté et les olives.",
            "Ajoutez les œufs coupés en quartiers.",
            "Servez frais."
        ],
        "image": "Salade niçoise.jpg"
    },
    {
        "title": "Taboulé libanais",
        "description": "Salade fraîche à base de boulgour, persil, tomates et citron.",
        "ingredients": [("Boulgour", 150, "g"), ("Tomates", 2, "pcs"), ("Persil", 1, "botte"), ("Citron", 1, "pcs"),
                        ("Oignon", 1, "pcs"), ("Menthe", 10, "feuilles")],
        "equip": ["Saladier", "Couteau"],
        "steps": [
            "Faites tremper le boulgour dans de l'eau froide 15 minutes.",
            "Hachez finement persil, menthe et oignon.",
            "Mélangez boulgour égoutté, herbes, tomates en dés et jus de citron.",
            "Assaisonnez d'huile d'olive, sel et poivre.",
            "Réfrigérez avant de servir."
        ],
        "image": "Taboulé libanais.png"
    },
    {
        "title": "Tian de légumes",
        "description": "Gratin de légumes méditerranéens en fines tranches, parfumé aux herbes.",
        "ingredients": [("Courgettes", 2, "pcs"), ("Aubergines", 2, "pcs"), ("Tomates", 3, "pcs"), ("Oignon", 1, "pcs")],
        "equip": ["Plat à gratin", "Couteau", "Four"],
        "steps": [
            "Coupez les légumes en fines rondelles.",
            "Disposez-les en couches alternées dans un plat à gratin.",
            "Arrosez d'huile d'olive et parsemez d'herbes de Provence.",
            "Cuisez au four à 180°C pendant 1 heure.",
            "Servez chaud ou tiède."
        ],
        "image": "Tian de légumes.jpg"
    },
    {
        "title": "Brochettes de poulet marinées",
        "description": "Brochettes grillées de poulet marinées au citron et aux herbes.",
        "ingredients": [("Poulet", 400, "g"), ("Citron", 1, "pcs"), ("Ail", 2, "gousses"), ("Persil", 1, "botte")],
        "equip": ["Barbecue", "Couteau", "Bol"],
        "steps": [
            "Préparez une marinade avec citron, ail, huile d'olive et persil.",
            "Coupez le poulet en cubes et laissez mariner 20 minutes.",
            "Enfilez les cubes de poulet sur des brochettes.",
            "Faites griller au barbecue 15 minutes.",
            "Servez avec une salade verte."
        ],
        "image": "Brochettes de poulet marinées.jpg"
    },
    {
        "title": "Gaspacho andalou",
        "description": "Soupe froide de légumes frais mixés, idéale pour se rafraîchir.",
        "ingredients": [("Tomates", 5, "pcs"), ("Concombre", 1, "pcs"), ("Poivron", 1, "pcs"), ("Oignon", 1, "pcs"), ("Pain", 50, "g")],
        "equip": ["Mixeur", "Saladier", "Couteau"],
        "steps": [
            "Coupez tomates, concombre, poivron et oignon.",
            "Mixez tous les légumes avec le pain rassis, huile d'olive et vinaigre.",
            "Salez, poivrez et réfrigérez pendant au moins 2 heures.",
            "Servez très frais."
        ],
        "image": "Gaspacho andalou.jpg"
    },
    {
        "title": "Ratatouille",
        "description": "Mijoté de légumes provençaux parfumé au thym et au basilic.",
        "ingredients": [("Oignon", 1, "pcs"), ("Ail", 2, "gousses"), ("Courgettes", 2, "pcs"), ("Aubergines", 2, "pcs"),
                        ("Tomates", 4, "pcs"), ("Poivron", 1, "pcs"), ("Basilic", 10, "feuilles")],
        "equip": ["Poêle", "Couteau", "Planche à découper"],
        "steps": [
            "Coupez tous les légumes en dés.",
            "Faites revenir oignons et ail dans de l'huile d'olive.",
            "Ajoutez les légumes et laissez mijoter 45 minutes.",
            "Assaisonnez avec thym, laurier et basilic.",
            "Servez chaud."
        ],
        "image": "Ratatouille.jpg"
    },
    {
        "title": "Poke bowl au saumon",
        "description": "Bol coloré avec saumon cru mariné, riz, légumes croquants et avocat.",
        "ingredients": [("Riz", 150, "g"), ("Saumon", 200, "g"), ("Avocat", 1, "pcs"), ("Concombre", 1, "pcs"), ("Maïs", 50, "g")],
        "equip": ["Bol", "Couteau"],
        "steps": [
            "Cuisez le riz et laissez-le refroidir.",
            "Coupez le saumon en dés et faites-le mariner (soja, citron, gingembre).",
            "Coupez avocat et concombre en dés.",
            "Disposez riz, saumon, légumes et maïs dans un bol.",
            "Ajoutez graines de sésame et sauce soja."
        ],
        "image": "Poke bowl au saumon.jpg"
    },
    {
        "title": "Quiche aux légumes d'été",
        "description": "Quiche légère aux courgettes, tomates et poivrons.",
        "ingredients": [("Pâtes", 1, "pâte brisée"), ("Courgettes", 2, "pcs"), ("Tomates", 2, "pcs"), ("Poivron", 1, "pcs"),
                        ("Œufs", 3, "pcs"), ("Crème fraîche", 200, "ml")],
        "equip": ["Moule à tarte", "Four", "Couteau"],
        "steps": [
            "Préparez une pâte brisée ou achetez-la prête.",
            "Coupez les légumes en petits morceaux et faites-les revenir.",
            "Étalez la pâte dans un moule, ajoutez légumes et mélange œufs-crème.",
            "Cuisez au four à 180°C pendant 35 minutes.",
            "Laissez tiédir avant de servir."
        ],
        "image": "Quiche aux légumes d'été.jpg"
    },
    {
        "title": "Salade de pâtes méditerranéenne",
        "description": "Salade froide de pâtes, olives, tomates séchées et mozzarella.",
        "ingredients": [("Pâtes", 200, "g"), ("Olives noires", 50, "g"), ("Tomates", 2, "pcs"), ("Mozzarella", 100, "g"), ("Basilic", 10, "feuilles")],
        "equip": ["Saladier", "Couteau"],
        "steps": [
            "Faites cuire les pâtes, égouttez et laissez refroidir.",
            "Coupez tomates et mozzarella en dés.",
            "Mélangez tous les ingrédients avec de l'huile d'olive.",
            "Assaisonnez sel, poivre et basilic.",
            "Servez frais."
        ],
        "image": "Salade de pâtes méditerranéenne.jpg"
    },
    {
        "title": "Pizza Margherita maison",
        "description": "Pizza fine et fraîche à la tomate, mozzarella et basilic.",
        "ingredients": [("Pâtes", 1, "pâte à pizza"), ("Tomates", 3, "pcs"), ("Mozzarella", 100, "g"), ("Basilic", 10, "feuilles")],
        "equip": ["Four", "Planche à découper", "Couteau"],
        "steps": [
            "Préparez la pâte à pizza et étalez-la finement.",
            "Étalez la sauce tomate puis ajoutez tranches de mozzarella.",
            "Cuisez au four à 220°C pendant 12-15 minutes.",
            "Parsemez de feuilles de basilic frais.",
            "Servez chaud."
        ],
        "image": "Pizza Margherita maison.jpg"
    }
]

# Générer des identifiants uniques à 5 chiffres pour chaque plat d'été
used_ids_ete_plats = set()
while len(used_ids_ete_plats) < len(plats_ete):
    new_id = random.randint(10000, 99999)
    if (new_id not in used_ids and
        new_id not in used_ids_automne and
        new_id not in used_ids_hiver and
        new_id not in used_ids_printemps and
        new_id not in used_ids_ete_plats):
        used_ids_ete_plats.add(new_id)
plats_ete_ids = list(used_ids_ete_plats)

for idx, plat in enumerate(plats_ete):
    recette_id = plats_ete_ids[idx]

    # Ajout recette
    cursor.execute("""
        INSERT INTO Recette (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recette_id,
        plat["title"],
        20,  # Preptime
        30,  # Cooktime
        "Plat",
        "Été",
        plat["description"],
        4,
        plat["image"]
    ))

    # Ajout étapes
    for num, step in enumerate(plat["steps"], start=1):
        cursor.execute("""
            INSERT INTO Step (Recette_id, Num_step, Contenu)
            VALUES (?, ?, ?)
        """, (recette_id, num, step))

    # Ajout ingrédients et quantités
    for name, valeur, unite in plat["ingredients"]:
        if name not in ingredient_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_ing_ids:
                    used_ing_ids.add(new_id)
                    ingredient_ids[name] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
                (ingredient_ids[name], name, allergenes_ete_plats.get(name, 0))
            )
        id_ing = ingredient_ids[name]
        cursor.execute("""
            INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
            VALUES (?, ?, ?, ?)
        """, (recette_id, id_ing, valeur, unite))

    # Ajout équipements
    for equip in plat["equip"]:
        if equip not in equipment_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_equip_ids:
                    used_equip_ids.add(new_id)
                    equipment_ids[equip] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
                (equipment_ids[equip], equip)
            )
        id_equip = equipment_ids[equip]
        cursor.execute("""
            INSERT INTO Recette_Equipment (Recette_id, Id_equipement)
            VALUES (?, ?)
        """, (recette_id, id_equip))

# PLATS AUTOMNE

ingredients_automne_plats = [
    "Potiron", "Champignons", "Poireaux", "Carottes", "Oignons", "Pommes de terre", "Lardons", "Crème fraîche", "Farine", "Beurre",
    "Vin rouge", "Sanglier", "Courge butternut", "Noisettes", "Châtaignes", "Porc", "Lentilles corail", "Cumin", "Pommes", "Filet mignon", "Fromage râpé", "Pâte brisée", "Bouillon de légumes"
]
allergenes_automne_plats = {
    "Crème fraîche": 1,
    "Farine": 1,
    "Beurre": 1,
    "Noisettes": 1,
    "Fromage râpé": 1,
    "Pâte brisée": 1
}

for name in ingredients_automne_plats:
    if name not in ingredient_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_ing_ids:
                used_ing_ids.add(new_id)
                ingredient_ids[name] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
            (ingredient_ids[name], name, allergenes_automne_plats.get(name, 0))
        )

equipments_automne_plats = [
    "Poêle", "Casserole", "Cuillère en bois", "Mixeur", "Four", "Moule à tarte", "Couteau", "Cocotte", "Plat à gratin", "Passoire"
]
for equip in equipments_automne_plats:
    if equip not in equipment_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_equip_ids:
                used_equip_ids.add(new_id)
                equipment_ids[equip] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
            (equipment_ids[equip], equip)
        )

plats_automne = [
    {
        "title": "Risotto aux champignons",
        "description": "Un risotto crémeux aux champignons forestiers, relevé au parmesan.",
        "ingredients": [("Champignons", 300, "g"), ("Riz", 200, "g"), ("Bouillon de légumes", 750, "ml"), ("Fromage râpé", 50, "g")],
        "equip": ["Poêle", "Casserole", "Cuillère en bois"],
        "steps": [
            "Faites revenir les champignons émincés dans du beurre.",
            "Ajoutez le riz et nacrez-le.",
            "Versez progressivement le bouillon en remuant.",
            "Incorporez le fromage râpé en fin de cuisson.",
            "Servez chaud et crémeux."
        ],
        "image": "Risotto aux champignons.jpg"
    },
    {
        "title": "Velouté de potiron",
        "description": "Soupe onctueuse de potiron, relevée avec une pointe de crème.",
        "ingredients": [("Potiron", 1, "kg"), ("Oignons", 1, "pcs"), ("Crème fraîche", 100, "ml")],
        "equip": ["Mixeur", "Casserole", "Couteau"],
        "steps": [
            "Épluchez et coupez le potiron en dés.",
            "Faites revenir l’oignon dans un peu d’huile.",
            "Ajoutez le potiron et couvrez d’eau.",
            "Laissez cuire 30 minutes puis mixez.",
            "Ajoutez la crème et assaisonnez."
        ],
        "image": "Velouté de potiron.jpg"
    },
    {
        "title": "Tarte aux poireaux",
        "description": "Tarte salée garnie de fondue de poireaux et crème fraîche.",
        "ingredients": [("Poireaux", 3, "pcs"), ("Pâte brisée", 1, "pâte"), ("Œufs", 3, "pcs"), ("Crème fraîche", 200, "ml")],
        "equip": ["Four", "Moule à tarte", "Couteau"],
        "steps": [
            "Lavez et émincez les poireaux.",
            "Faites-les revenir dans du beurre jusqu’à ce qu’ils fondent.",
            "Battez œufs et crème, salez, poivrez.",
            "Garnissez une pâte brisée avec poireaux et appareil.",
            "Enfournez 35 min à 180°C."
        ],
        "image": "Tarte aux poireaux.jpg"
    },
    {
        "title": "Civet de sanglier",
        "description": "Plat mijoté de sanglier mariné au vin rouge et aromates.",
        "ingredients": [("Sanglier", 1.2, "kg"), ("Vin rouge", 750, "ml"), ("Carottes", 3, "pcs"), ("Oignons", 2, "pcs"), ("Champignons", 300, "g")],
        "equip": ["Cocotte", "Couteau", "Passoire"],
        "steps": [
            "Faites mariner la viande avec vin rouge, carottes, oignons et thym pendant 12h.",
            "Égouttez, puis faites revenir la viande.",
            "Ajoutez la marinade filtrée et laissez mijoter 3h.",
            "Ajoutez les champignons en fin de cuisson.",
            "Servez bien chaud avec des pâtes fraîches."
        ],
        "image": "Civet de sanglier.jpg"
    },
    {
        "title": "Gratin de courge butternut",
        "description": "Gratin fondant à base de courge butternut, crème et fromage.",
        "ingredients": [("Courge butternut", 1, "kg"), ("Crème fraîche", 200, "ml"), ("Fromage râpé", 100, "g")],
        "equip": ["Four", "Plat à gratin", "Couteau"],
        "steps": [
            "Pelez et coupez la courge en dés.",
            "Faites-la cuire à l’eau puis égouttez.",
            "Mélangez avec crème, fromage râpé, sel, poivre.",
            "Versez dans un plat à gratin et enfournez 45 min.",
            "Servez doré et chaud."
        ],
        "image": "Gratin de courge butternut.jpg"
    },
    {
        "title": "Quiche aux champignons et noisettes",
        "description": "Quiche originale aux champignons sautés et éclats de noisette.",
        "ingredients": [("Champignons", 300, "g"), ("Oignons", 1, "pcs"), ("Noisettes", 50, "g"), ("Œufs", 2, "pcs"), ("Crème fraîche", 150, "ml")],
        "equip": ["Poêle", "Four", "Moule à tarte"],
        "steps": [
            "Nettoyez et émincez les champignons.",
            "Faites-les revenir avec les oignons.",
            "Concassez les noisettes grossièrement.",
            "Garnissez une pâte avec champignons, noisettes et appareil œufs/crème.",
            "Enfournez 40 min à 180°C."
        ],
        "image": "Quiche aux champignons et noisettes.jpg"
    },
    {
        "title": "Poêlée de châtaignes et lardons",
        "description": "Poêlée rustique à base de châtaignes, lardons et oignons.",
        "ingredients": [("Châtaignes", 400, "g"), ("Lardons", 150, "g"), ("Oignons", 1, "pcs")],
        "equip": ["Poêle", "Couteau"],
        "steps": [
            "Faites revenir les lardons et oignons dans une poêle.",
            "Ajoutez les châtaignes et laissez dorer.",
            "Assaisonnez avec poivre et herbes de Provence.",
            "Servez chaud en accompagnement ou plat principal."
        ],
        "image": "Poêlée de châtaignes et lardons.jpg"
    },
    {
        "title": "Gratin de macaronis au potiron",
        "description": "Macaronis gratinés avec une sauce onctueuse au potiron.",
        "ingredients": [("Pâtes", 250, "g"), ("Potiron", 300, "g"), ("Crème fraîche", 200, "ml"), ("Fromage râpé", 100, "g")],
        "equip": ["Casserole", "Four", "Plat à gratin"],
        "steps": [
            "Faites cuire les macaronis.",
            "Faites revenir le potiron en dés dans une casserole.",
            "Ajoutez crème et épices, mixez en purée.",
            "Mélangez avec les pâtes, versez dans un plat.",
            "Ajoutez fromage râpé et gratinez 20 min."
        ],
        "image": "Gratin de macaronis au potiron.jpg"
    },
    {
        "title": "Soupe de lentilles corail et carottes",
        "description": "Soupe épaisse à base de lentilles corail et carottes, parfumée au cumin.",
        "ingredients": [("Lentilles corail", 200, "g"), ("Carottes", 3, "pcs"), ("Oignons", 1, "pcs"), ("Cumin", 1, "c. à café")],
        "equip": ["Casserole", "Mixeur", "Couteau"],
        "steps": [
            "Faites revenir un oignon émincé.",
            "Ajoutez les carottes en rondelles et les lentilles.",
            "Couvrez d’eau et assaisonnez.",
            "Laissez cuire 30 min à feu doux.",
            "Mixez selon la texture souhaitée."
        ],
        "image": "Soupe de lentilles corail et carottes.jpg"
    },
    {
        "title": "Filet mignon aux pommes",
        "description": "Filet mignon de porc rôti, accompagné de pommes caramélisées.",
        "ingredients": [("Filet mignon", 600, "g"), ("Pommes", 3, "pcs"), ("Beurre", 30, "g"), ("Vin rouge", 100, "ml")],
        "equip": ["Poêle", "Couteau"],
        "steps": [
            "Faites revenir le filet mignon dans du beurre.",
            "Ajoutez les pommes épluchées et coupées en quartiers.",
            "Versez un peu de vin rouge pour la cuisson.",
            "Laissez mijoter 40 min à feu doux.",
            "Servez nappé de sauce aux pommes."
        ],
        "image": "Filet mignon aux pommes.jpg"
    }
]

# Générer des identifiants uniques à 5 chiffres pour chaque plat d'automne
used_ids_automne_plats = set()
while len(used_ids_automne_plats) < len(plats_automne):
    new_id = random.randint(10000, 99999)
    if (new_id not in used_ids and
        new_id not in used_ids_automne and
        new_id not in used_ids_hiver and
        new_id not in used_ids_printemps and
        new_id not in used_ids_ete_plats and
        new_id not in used_ids_automne_plats):
        used_ids_automne_plats.add(new_id)
plats_automne_ids = list(used_ids_automne_plats)

for idx, plat in enumerate(plats_automne):
    recette_id = plats_automne_ids[idx]

    # Ajout recette
    cursor.execute("""
        INSERT INTO Recette (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recette_id,
        plat["title"],
        25,  # Preptime
        45,  # Cooktime
        "Plat",
        "Automne",
        plat["description"],
        4,
        plat["image"]
    ))

    # Ajout étapes
    for num, step in enumerate(plat["steps"], start=1):
        cursor.execute("""
            INSERT INTO Step (Recette_id, Num_step, Contenu)
            VALUES (?, ?, ?)
        """, (recette_id, num, step))

    # Ajout ingrédients et quantités
    for name, valeur, unite in plat["ingredients"]:
        if name not in ingredient_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_ing_ids:
                    used_ing_ids.add(new_id)
                    ingredient_ids[name] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
                (ingredient_ids[name], name, allergenes_automne_plats.get(name, 0))
            )
        id_ing = ingredient_ids[name]
        cursor.execute("""
            INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
            VALUES (?, ?, ?, ?)
        """, (recette_id, id_ing, valeur, unite))

    # Ajout équipements
    for equip in plat["equip"]:
        if equip not in equipment_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_equip_ids:
                    used_equip_ids.add(new_id)
                    equipment_ids[equip] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
                (equipment_ids[equip], equip)
            )
        id_equip = equipment_ids[equip]
        cursor.execute("""
            INSERT INTO Recette_Equipment (Recette_id, Id_equipement)
            VALUES (?, ?)
        """, (recette_id, id_equip))

# PLATS HIVER

ingredients_hiver_plats = [
    "Pommes de terre", "Chou vert", "Carottes", "Oignons", "Saucisse fumée", "Lard fumé", "Bœuf", "Vin rouge", "Champignons", "Ail",
    "Crème fraîche", "Beurre", "Farine", "Lait", "Reblochon", "Viande hachée", "Haricots rouges", "Tomates concassées", "Épices chili",
    "Haricots blancs", "Confit de canard", "Saucisse de Toulouse", "Porc", "Pain", "Gruyère râpé", "Charcuterie variée", "Cornichons"
]
allergenes_hiver_plats = {
    "Crème fraîche": 1,
    "Beurre": 1,
    "Farine": 1,
    "Lait": 1,
    "Reblochon": 1,
    "Gruyère râpé": 1,
    "Pain": 1
}

for name in ingredients_hiver_plats:
    if name not in ingredient_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_ing_ids:
                used_ing_ids.add(new_id)
                ingredient_ids[name] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
            (ingredient_ids[name], name, allergenes_hiver_plats.get(name, 0))
        )

equipments_hiver_plats = [
    "Cocotte", "Couteau", "Planche à découper", "Plat à gratin", "Four", "Casserole", "Gril du four", "Poêle", "Cuillère en bois", "Appareil à raclette", "Fourchette"
]
for equip in equipments_hiver_plats:
    if equip not in equipment_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_equip_ids:
                used_equip_ids.add(new_id)
                equipment_ids[equip] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
            (equipment_ids[equip], equip)
        )

plats_hiver = [
    {
        "title": "Potée auvergnate",
        "description": "Un classique plat mijoté avec choux, pommes de terre et viandes fumées.",
        "ingredients": [("Chou vert", 1, "pcs"), ("Pommes de terre", 800, "g"), ("Saucisse fumée", 300, "g"), ("Lard fumé", 200, "g"), ("Carottes", 3, "pcs")],
        "equip": ["Cocotte", "Couteau", "Planche à découper"],
        "steps": [
            "Coupez les légumes et préparez les viandes fumées.",
            "Faites revenir les viandes dans une grande cocotte.",
            "Ajoutez les légumes et recouvrez d'eau.",
            "Laissez mijoter à feu doux pendant 2 heures.",
            "Servez chaud avec de la moutarde."
        ],
        "image": "Potée auvergnate.jpg"
    },
    {
        "title": "Gratin dauphinois",
        "description": "Pommes de terre fondantes à la crème et à l'ail, gratinées au four.",
        "ingredients": [("Pommes de terre", 800, "g"), ("Crème fraîche", 300, "ml"), ("Ail", 2, "gousses"), ("Beurre", 30, "g")],
        "equip": ["Plat à gratin", "Couteau", "Four"],
        "steps": [
            "Épluchez et coupez les pommes de terre en fines rondelles.",
            "Frottez un plat à gratin avec de l'ail.",
            "Disposez les pommes de terre en couches dans le plat.",
            "Versez la crème et ajoutez sel, poivre et muscade.",
            "Faites cuire au four à 160°C pendant 1h30."
        ],
        "image": "Gratin dauphinois.jpg"
    },
    {
        "title": "Soupe à l'oignon gratinée",
        "description": "Soupe riche en oignons caramélisés, gratinée au fromage.",
        "ingredients": [("Oignons", 5, "pcs"), ("Bouillon de bœuf", 1, "l"), ("Gruyère râpé", 150, "g"), ("Pain", 4, "tranches")],
        "equip": ["Casserole", "Gril du four", "Couteau"],
        "steps": [
            "Émincez les oignons et faites-les revenir jusqu'à caramélisation.",
            "Ajoutez du bouillon de bœuf et laissez mijoter.",
            "Versez la soupe dans des bols.",
            "Disposez des tranches de pain grillé et du gruyère râpé dessus.",
            "Passez sous le gril du four jusqu'à gratinage."
        ],
        "image": "Soupe à l'oignon gratinée.jpg"
    },
    {
        "title": "Bœuf bourguignon",
        "description": "Ragoût de bœuf mijoté au vin rouge, carottes et champignons.",
        "ingredients": [("Bœuf", 1.5, "kg"), ("Vin rouge", 750, "ml"), ("Carottes", 4, "pcs"), ("Champignons", 300, "g"), ("Oignons", 2, "pcs")],
        "equip": ["Cocotte", "Couteau", "Planche à découper"],
        "steps": [
            "Coupez le bœuf en morceaux et faites-les revenir dans de l'huile.",
            "Ajoutez carottes, oignons, ail, vin rouge et bouquet garni.",
            "Laissez mijoter doucement 3 heures.",
            "Ajoutez les champignons en fin de cuisson.",
            "Servez bien chaud."
        ], 
        "image": "Bœuf bourguignon.jpg"
    },
    {
        "title": "Tartiflette savoyarde",
        "description": "Gratin savoyard avec pommes de terre, reblochon et lardons.",
        "ingredients": [("Pommes de terre", 1, "kg"), ("Reblochon", 450, "g"), ("Lardons", 150, "g"), ("Oignons", 1, "pcs")],
        "equip": ["Plat à gratin", "Couteau", "Poêle"],
        "steps": [
            "Faites cuire les pommes de terre à l'eau puis coupez-les en tranches.",
            "Faites revenir les lardons et les oignons.",
            "Dans un plat, alternez pommes de terre, lardons, oignons et reblochon.",
            "Cuisez au four à 180°C pendant 1 heure.",
            "Servez chaud."
        ],
        "image": "Tartiflette savoyarde.jpg"
    },
    {
        "title": "Chili con carne",
        "description": "Plat tex-mex épicé à base de viande, haricots rouges et tomates.",
        "ingredients": [("Viande hachée", 600, "g"), ("Haricots rouges", 400, "g"), ("Tomates concassées", 500, "g"), ("Oignons", 1, "pcs"), ("Épices chili", 1, "c. à soupe")],
        "equip": ["Casserole", "Cuillère en bois", "Couteau"],
        "steps": [
            "Faites revenir la viande hachée avec les oignons et épices.",
            "Ajoutez les haricots rouges, tomates et laissez mijoter 1 heure.",
            "Rectifiez l'assaisonnement.",
            "Servez avec du riz."
        ],
        "image": "Chili con carne.jpg"
    },
    {
        "title": "Cassoulet traditionnel",
        "description": "Ragoût de haricots blancs, confit de canard, saucisse et porc.",
        "ingredients": [("Haricots blancs", 500, "g"), ("Confit de canard", 600, "g"), ("Saucisse de Toulouse", 400, "g"), ("Porc", 300, "g")],
        "equip": ["Cocotte", "Couteau", "Planche à découper"],
        "steps": [
            "Faites tremper les haricots la veille.",
            "Faites cuire les viandes et haricots séparément.",
            "Assemblez dans une grande cocotte et laissez mijoter 4 heures.",
            "Servez très chaud."
        ],
        "image": "Cassoulet traditionnel.jpg"
    },
    {
        "title": "Velouté de potimarron",
        "description": "Soupe veloutée à base de potimarron, douce et parfumée.",
        "ingredients": [("Potimarron", 1, "kg"), ("Ail", 1, "gousse"), ("Crème fraîche", 200, "ml"), ("Oignon", 1, "pcs")],
        "equip": ["Casserole", "Mixeur", "Couteau"],
        "steps": [
            "Épluchez et coupez le potimarron.",
            "Faites revenir avec un oignon.",
            "Ajoutez bouillon et laissez cuire 30 minutes.",
            "Mixez la soupe, ajoutez crème et assaisonnez.",
            "Servez chaud."
        ],
        "image": "Velouté de potimarron.jpg"
    },
    {
        "title": "Parmentier de confit de canard",
        "description": "Hachis de confit de canard sous une purée de pommes de terre gratinée.",
        "ingredients": [("Confit de canard", 600, "g"), ("Pommes de terre", 800, "g"), ("Beurre", 50, "g"), ("Lait", 100, "ml")],
        "equip": ["Plat à gratin", "Four", "Couteau"],
        "steps": [
            "Effilochez le confit de canard.",
            "Préparez une purée de pommes de terre.",
            "Dans un plat, mettez le confit puis recouvrez de purée.",
            "Faites gratiner au four 20 minutes.",
            "Servez chaud."
        ],
        "image": "Parmentier de confit de canard.jpg"
    },
    {
        "title": "Raclette traditionnelle",
        "description": "Fromage fondu servi avec pommes de terre, charcuterie et cornichons.",
        "ingredients": [("Reblochon", 600, "g"), ("Pommes de terre", 1, "kg"), ("Charcuterie variée", 300, "g"), ("Cornichons", 100, "g")],
        "equip": ["Appareil à raclette", "Couteau", "Fourchette"],
        "steps": [
            "Faites cuire les pommes de terre à l'eau.",
            "Disposez le fromage à raclette sur un appareil chauffant.",
            "Faites fondre le fromage et servez avec charcuterie et cornichons.",
            "Chacun compose son assiette."
        ],
        "image": "Raclette traditionnelle.jpg"
    }
]

# Générer des identifiants uniques à 5 chiffres pour chaque plat d'hiver
used_ids_hiver_plats = set()
while len(used_ids_hiver_plats) < len(plats_hiver):
    new_id = random.randint(10000, 99999)
    if (new_id not in used_ids and
        new_id not in used_ids_automne and
        new_id not in used_ids_hiver and
        new_id not in used_ids_printemps and
        new_id not in used_ids_ete_plats and
        new_id not in used_ids_automne_plats and
        new_id not in used_ids_hiver_plats):
        used_ids_hiver_plats.add(new_id)
plats_hiver_ids = list(used_ids_hiver_plats)

for idx, plat in enumerate(plats_hiver):
    recette_id = plats_hiver_ids[idx]

    # Ajout recette
    cursor.execute("""
        INSERT INTO Recette (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recette_id,
        plat["title"],
        30,  # Preptime
        90,  # Cooktime
        "Plat",
        "Hiver",
        plat["description"],
        4,
        plat["image"]
    ))

    # Ajout étapes
    for num, step in enumerate(plat["steps"], start=1):
        cursor.execute("""
            INSERT INTO Step (Recette_id, Num_step, Contenu)
            VALUES (?, ?, ?)
        """, (recette_id, num, step))

    # Ajout ingrédients et quantités
    for name, valeur, unite in plat["ingredients"]:
        if name not in ingredient_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_ing_ids:
                    used_ing_ids.add(new_id)
                    ingredient_ids[name] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
                (ingredient_ids[name], name, allergenes_hiver_plats.get(name, 0))
            )
        id_ing = ingredient_ids[name]
        cursor.execute("""
            INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
            VALUES (?, ?, ?, ?)
        """, (recette_id, id_ing, valeur, unite))

    # Ajout équipements
    for equip in plat["equip"]:
        if equip not in equipment_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_equip_ids:
                    used_equip_ids.add(new_id)
                    equipment_ids[equip] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
                (equipment_ids[equip], equip)
            )
        id_equip = equipment_ids[equip]
        cursor.execute("""
            INSERT INTO Recette_Equipment (Recette_id, Id_equipement)
            VALUES (?, ?)
        """, (recette_id, id_equip))

# PLATS PRINTEMPS

ingredients_printemps_plats = [
    "Asperges", "Petits pois", "Carottes", "Oignons", "Poulet", "Citron", "Menthe", "Laitue", "Radis", "Fèves",
    "Pommes de terre", "Saumon", "Épinards", "Crème fraîche", "Pâtes", "Parmesan", "Courgettes", "Basilic", "Riz", "Fromage frais"
]
allergenes_printemps_plats = {
    "Crème fraîche": 1,
    "Pâtes": 1,
    "Parmesan": 1,
    "Fromage frais": 1
}

for name in ingredients_printemps_plats:
    if name not in ingredient_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_ing_ids:
                used_ing_ids.add(new_id)
                ingredient_ids[name] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
            (ingredient_ids[name], name, allergenes_printemps_plats.get(name, 0))
        )

equipments_printemps_plats = [
    "Casserole", "Poêle", "Saladier", "Couteau", "Planche à découper", "Four", "Mixeur", "Moule à tarte", "Cuillère en bois", "Passoire"
]
for equip in equipments_printemps_plats:
    if equip not in equipment_ids:
        while True:
            new_id = random.randint(10000, 99999)
            if new_id not in used_equip_ids:
                used_equip_ids.add(new_id)
                equipment_ids[equip] = new_id
                break
        cursor.execute(
            "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
            (equipment_ids[equip], equip)
        )

plats_printemps = [
    {
        "title": "Salade de printemps",
        "description": "Salade croquante aux asperges, radis, petits pois et vinaigrette citronnée.",
        "ingredients": [("Asperges", 300, "g"), ("Radis", 1, "botte"), ("Petits pois", 100, "g"), ("Laitue", 1, "pcs"), ("Citron", 1, "pcs")],
        "equip": ["Saladier", "Couteau", "Planche à découper"],
        "steps": [
            "Faites cuire les asperges et les petits pois.",
            "Émincez les radis et la laitue.",
            "Mélangez tous les légumes dans un saladier.",
            "Préparez une vinaigrette au citron.",
            "Servez frais."
        ],
        "image": "Salade de printemps.jpg"
    },
    {
        "title": "Risotto aux asperges et petits pois",
        "description": "Risotto crémeux aux asperges vertes et petits pois frais.",
        "ingredients": [("Riz", 200, "g"), ("Asperges", 200, "g"), ("Petits pois", 100, "g"), ("Oignons", 1, "pcs"), ("Parmesan", 50, "g")],
        "equip": ["Casserole", "Poêle", "Cuillère en bois"],
        "steps": [
            "Faites revenir l'oignon émincé dans un peu d'huile.",
            "Ajoutez le riz et nacrez-le.",
            "Ajoutez les asperges coupées et les petits pois.",
            "Versez le bouillon petit à petit jusqu'à cuisson du riz.",
            "Ajoutez le parmesan en fin de cuisson."
        ],
        "image": "Risotto aux asperges et petits pois.png"
    },
    {
        "title": "Tarte aux épinards et fromage frais",
        "description": "Tarte salée printanière aux épinards et fromage frais.",
        "ingredients": [("Épinards", 300, "g"), ("Pâtes", 1, "pâte brisée"), ("Fromage frais", 150, "g"), ("Oignons", 1, "pcs"), ("Œufs", 2, "pcs")],
        "equip": ["Four", "Moule à tarte", "Couteau"],
        "steps": [
            "Faites revenir les épinards et l'oignon.",
            "Mélangez avec le fromage frais et les œufs.",
            "Étalez la pâte dans un moule et garnissez avec la préparation.",
            "Faites cuire 30 min à 180°C.",
            "Servez tiède."
        ],
        "image": "Tarte aux épinards et fromage frais.jpg"
    },
    {
        "title": "Poulet au citron et aux herbes",
        "description": "Blancs de poulet marinés au citron, cuits à la poêle avec des herbes fraîches.",
        "ingredients": [("Poulet", 400, "g"), ("Citron", 1, "pcs"), ("Menthe", 5, "feuilles"), ("Basilic", 5, "feuilles")],
        "equip": ["Poêle", "Couteau"],
        "steps": [
            "Préparez une marinade avec citron, menthe et basilic.",
            "Faites mariner le poulet 20 minutes.",
            "Faites cuire à la poêle jusqu'à ce qu'il soit doré.",
            "Servez avec une salade verte."
        ],
        "image": "Poulet au citron et aux herbes.jpg"
    },
    {
        "title": "Pâtes aux courgettes et basilic",
        "description": "Pâtes fraîches sautées avec des courgettes et du basilic.",
        "ingredients": [("Pâtes", 200, "g"), ("Courgettes", 2, "pcs"), ("Basilic", 10, "feuilles"), ("Parmesan", 40, "g")],
        "equip": ["Casserole", "Poêle", "Couteau"],
        "steps": [
            "Faites cuire les pâtes.",
            "Faites revenir les courgettes en dés dans une poêle.",
            "Ajoutez les pâtes égouttées et le basilic.",
            "Parsemez de parmesan avant de servir."
        ],
        "image": "Pâtes aux courgettes et basilic.jpg"
    },
    {
        "title": "Saumon en papillote",
        "description": "Filets de saumon cuits en papillote avec citron et herbes.",
        "ingredients": [("Saumon", 2, "pcs"), ("Citron", 1, "pcs"), ("Menthe", 5, "feuilles"), ("Basilic", 5, "feuilles")],
        "equip": ["Four", "Couteau"],
        "steps": [
            "Déposez les filets de saumon sur du papier cuisson.",
            "Ajoutez des rondelles de citron et les herbes.",
            "Fermez la papillote et enfournez 20 min à 180°C.",
            "Servez avec du riz ou des légumes."
        ],
        "image": "Saumon en papillote.jpg"
    },
    {
        "title": "Poêlée de fèves et carottes",
        "description": "Fèves fraîches et carottes nouvelles sautées à la poêle.",
        "ingredients": [("Fèves", 200, "g"), ("Carottes", 3, "pcs"), ("Oignons", 1, "pcs"), ("Menthe", 5, "feuilles")],
        "equip": ["Poêle", "Couteau"],
        "steps": [
            "Écossez les fèves.",
            "Faites revenir l'oignon et les carottes en rondelles.",
            "Ajoutez les fèves et la menthe.",
            "Laissez cuire 15 minutes.",
            "Servez chaud."
        ],
        "image": "Poêlée de fèves et carottes.jpg"
    },
    {
        "title": "Omelette aux herbes fraîches",
        "description": "Omelette moelleuse aux herbes du printemps.",
        "ingredients": [("Œufs", 4, "pcs"), ("Menthe", 5, "feuilles"), ("Basilic", 5, "feuilles"), ("Oignons", 1, "pcs")],
        "equip": ["Poêle", "Couteau"],
        "steps": [
            "Battez les œufs avec les herbes ciselées.",
            "Faites revenir l'oignon émincé.",
            "Versez les œufs battus et laissez cuire doucement.",
            "Servez chaud ou froid."
        ],
        "image": "Omelette aux herbes fraîches.jpg"
    },
    {
        "title": "Salade de pommes de terre et radis",
        "description": "Salade fraîche de pommes de terre, radis et herbes.",
        "ingredients": [("Pommes de terre", 500, "g"), ("Radis", 1, "botte"), ("Menthe", 5, "feuilles"), ("Citron", 1, "pcs")],
        "equip": ["Casserole", "Saladier", "Couteau"],
        "steps": [
            "Faites cuire les pommes de terre et coupez-les en dés.",
            "Émincez les radis.",
            "Mélangez avec la menthe et le jus de citron.",
            "Servez frais."
        ],
        "image": "Salade de pommes de terre et radis.jpg"
    },
    {
        "title": "Gratin de courgettes et pommes de terre",
        "description": "Gratin léger de courgettes et pommes de terre à la crème.",
        "ingredients": [("Courgettes", 2, "pcs"), ("Pommes de terre", 400, "g"), ("Crème fraîche", 150, "ml"), ("Parmesan", 40, "g")],
        "equip": ["Four", "Plat à gratin", "Couteau"],
        "steps": [
            "Coupez les courgettes et pommes de terre en rondelles.",
            "Disposez-les dans un plat à gratin.",
            "Ajoutez la crème et le parmesan.",
            "Faites cuire 35 min à 180°C.",
            "Servez chaud."
        ],
        "image": "Gratin de courgettes et pommes de terre.jpg"
    },
    {
        "title": "Riz aux petits pois et menthe",
        "description": "Riz parfumé aux petits pois et à la menthe fraîche.",
        "ingredients": [("Riz", 200, "g"), ("Petits pois", 100, "g"), ("Menthe", 5, "feuilles"), ("Oignons", 1, "pcs")],
        "equip": ["Casserole", "Couteau"],
        "steps": [
            "Faites cuire le riz et les petits pois.",
            "Faites revenir l'oignon émincé.",
            "Mélangez le tout avec la menthe ciselée.",
            "Servez chaud ou froid."
        ],
        "image": "Riz aux petits pois et menthe.jpg"
    }
]

# Générer des identifiants uniques à 5 chiffres pour chaque plat de printemps
used_ids_printemps_plats = set()
while len(used_ids_printemps_plats) < len(plats_printemps):
    new_id = random.randint(10000, 99999)
    if (new_id not in used_ids and
        new_id not in used_ids_automne and
        new_id not in used_ids_hiver and
        new_id not in used_ids_printemps and
        new_id not in used_ids_ete_plats and
        new_id not in used_ids_automne_plats and
        new_id not in used_ids_hiver_plats and
        new_id not in used_ids_printemps_plats):
        used_ids_printemps_plats.add(new_id)
plats_printemps_ids = list(used_ids_printemps_plats)

for idx, plat in enumerate(plats_printemps):
    recette_id = plats_printemps_ids[idx]

    # Ajout recette
    cursor.execute("""
        INSERT INTO Recette (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recette_id,
        plat["title"],
        20,  # Preptime
        30,  # Cooktime
        "Plat",
        "Printemps",
        plat["description"],
        4,
        plat["image"]
    ))

    # Ajout étapes
    for num, step in enumerate(plat["steps"], start=1):
        cursor.execute("""
            INSERT INTO Step (Recette_id, Num_step, Contenu)
            VALUES (?, ?, ?)
        """, (recette_id, num, step))

    # Ajout ingrédients et quantités
    for name, valeur, unite in plat["ingredients"]:
        if name not in ingredient_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_ing_ids:
                    used_ing_ids.add(new_id)
                    ingredient_ids[name] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Ingredient (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
                (ingredient_ids[name], name, allergenes_printemps_plats.get(name, 0))
            )
        id_ing = ingredient_ids[name]
        cursor.execute("""
            INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
            VALUES (?, ?, ?, ?)
        """, (recette_id, id_ing, valeur, unite))

    # Ajout équipements
    for equip in plat["equip"]:
        if equip not in equipment_ids:
            while True:
                new_id = random.randint(10000, 99999)
                if new_id not in used_equip_ids:
                    used_equip_ids.add(new_id)
                    equipment_ids[equip] = new_id
                    break
            cursor.execute(
                "INSERT OR IGNORE INTO Equipment (Id_equipement, Name) VALUES (?, ?)",
                (equipment_ids[equip], equip)
            )
        id_equip = equipment_ids[equip]
        cursor.execute("""
            INSERT INTO Recette_Equipment (Recette_id, Id_equipement)
            VALUES (?, ?)
        """, (recette_id, id_equip))

# Sauvegarde les changements et ferme la connexion
conn.commit()
conn.close()