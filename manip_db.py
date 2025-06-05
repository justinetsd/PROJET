import sqlite3, random

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

### AJOUT DES RECETTES --------------------------------------------------------------------------------------------------------------

    ## PLATS HIVER

# recettes_hiver = [
#     (2, "Potée auvergnate", 30, 120, "Plat", "Hiver",
#      "Un classique plat mijoté avec choux, pommes de terre et viandes fumées.", 6, "potee_auvergnate.jpg"),
#     (3, "Gratin dauphinois", 20, 90, "Plat", "Hiver",
#      "Pommes de terre fondantes à la crème et à l'ail, gratinées au four.", 4, "gratin_dauphinois.jpg"),
#     (4, "Soupe à l'oignon gratinée", 15, 45, "Entrée", "Hiver",
#      "Soupe riche en oignons caramélisés, gratinée au fromage.", 4, "soupe_oignon.jpg"),
#     (5, "Bœuf bourguignon", 40, 180, "Plat", "Hiver",
#      "Ragoût de bœuf mijoté au vin rouge, carottes et champignons.", 6, "boeuf_bourguignon.jpg"),
#     (6, "Tartiflette savoyarde", 25, 60, "Plat", "Hiver",
#      "Gratin savoyard avec pommes de terre, reblochon et lardons.", 4, "tartiflette.jpg"),
#     (7, "Chili con carne", 25, 90, "Plat", "Hiver",
#      "Plat tex-mex épicé à base de viande, haricots rouges et tomates.", 5, "chili_con_carne.jpg"),
#     (8, "Cassoulet traditionnel", 60, 240, "Plat", "Hiver",
#      "Ragoût de haricots blancs, confit de canard, saucisse et porc.", 6, "cassoulet.jpg"),
#     (9, "Velouté de potimarron", 20, 30, "Entrée", "Hiver",
#      "Soupe veloutée à base de potimarron, douce et parfumée.", 4, "veloute_potimarron.jpg"),
#     (10, "Parmentier de confit de canard", 30, 60, "Plat", "Hiver",
#      "Hachis de confit de canard sous une purée de pommes de terre gratinée.", 4, "parmentier.jpg"),
#     (11, "Raclette traditionnelle", 10, 20, "Plat", "Hiver",
#      "Fromage fondu servi avec pommes de terre, charcuterie et cornichons.", 4, "raclette.jpg"),
# ]

# for r in recettes_hiver:
#     cursor.execute("""
#     INSERT INTO Recettes (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, r)

# # Étapes de préparation pour chaque recette (exemple simplifié, en général 4-6 étapes)
# steps_dict = {
#     2: [
#         "Coupez les légumes et préparez les viandes fumées.",
#         "Faites revenir les viandes dans une grande cocotte.",
#         "Ajoutez les légumes et recouvrez d'eau.",
#         "Laissez mijoter à feu doux pendant 2 heures.",
#         "Servez chaud avec de la moutarde."
#     ],
#     3: [
#         "Épluchez et coupez les pommes de terre en fines rondelles.",
#         "Frottez un plat à gratin avec de l'ail.",
#         "Disposez les pommes de terre en couches dans le plat.",
#         "Versez la crème et ajoutez sel, poivre et muscade.",
#         "Faites cuire au four à 160°C pendant 1h30."
#     ],
#     4: [
#         "Émincez les oignons et faites-les revenir jusqu'à caramélisation.",
#         "Ajoutez du bouillon de bœuf et laissez mijoter.",
#         "Versez la soupe dans des bols.",
#         "Disposez des tranches de pain grillé et du gruyère râpé dessus.",
#         "Passez sous le gril du four jusqu'à gratinage."
#     ],
#     5: [
#         "Coupez le bœuf en morceaux et faites-les revenir dans de l'huile.",
#         "Ajoutez carottes, oignons, ail, vin rouge et bouquet garni.",
#         "Laissez mijoter doucement 3 heures.",
#         "Ajoutez les champignons en fin de cuisson.",
#         "Servez bien chaud."
#     ],
#     6: [
#         "Faites cuire les pommes de terre à l'eau puis coupez-les en tranches.",
#         "Faites revenir les lardons et les oignons.",
#         "Dans un plat, alternez pommes de terre, lardons, oignons et reblochon.",
#         "Cuisez au four à 180°C pendant 1 heure.",
#         "Servez chaud."
#     ],
#     7: [
#         "Faites revenir la viande hachée avec les oignons et épices.",
#         "Ajoutez les haricots rouges, tomates et laissez mijoter 1 heure.",
#         "Rectifiez l'assaisonnement.",
#         "Servez avec du riz."
#     ],
#     8: [
#         "Faites tremper les haricots la veille.",
#         "Faites cuire les viandes et haricots séparément.",
#         "Assemblez dans une grande cocotte et laissez mijoter 4 heures.",
#         "Servez très chaud."
#     ],
#     9: [
#         "Épluchez et coupez le potimarron.",
#         "Faites revenir avec un oignon.",
#         "Ajoutez bouillon et laissez cuire 30 minutes.",
#         "Mixez la soupe, ajoutez crème et assaisonnez.",
#         "Servez chaud."
#     ],
#     10: [
#         "Effilochez le confit de canard.",
#         "Préparez une purée de pommes de terre.",
#         "Dans un plat, mettez le confit puis recouvrez de purée.",
#         "Faites gratiner au four 20 minutes.",
#         "Servez chaud."
#     ],
#     11: [
#         "Faites cuire les pommes de terre à l'eau.",
#         "Disposez le fromage à raclette sur un appareil chauffant.",
#         "Faites fondre le fromage et servez avec charcuterie et cornichons.",
#         "Chacun compose son assiette."
#     ]
# }

# for rid, steps in steps_dict.items():
#     for i, contenu in enumerate(steps, start=1):
#         cursor.execute("""
#         INSERT INTO Steps (Recette_id, Num_step, Contenu)
#         VALUES (?, ?, ?)
#         """, (rid, i, contenu))

# # Ingrédients pour chaque recette (exemple simplifié, Id_ingredient doit être unique dans la base)
# ingredients_dict = {
#     2: [(6, "Chou vert", False), (7, "Pommes de terre", False), (8, "Saucisse fumée", False), (9, "Lard fumé", False), (10, "Carottes", False)],
#     3: [(7, "Pommes de terre", False), (11, "Crème fraîche", False), (12, "Ail", False), (13, "Beurre", False)],
#     4: [(14, "Oignons", False), (15, "Bouillon de bœuf", False), (16, "Gruyère râpé", True), (17, "Pain", False)],
#     5: [(18, "Bœuf", False), (19, "Vin rouge", False), (20, "Carottes", False), (21, "Champignons", False), (22, "Oignons", False)],
#     6: [(7, "Pommes de terre", False), (23, "Reblochon", True), (24, "Lardons", False), (22, "Oignons", False)],
#     7: [(25, "Viande hachée", False), (26, "Haricots rouges", False), (27, "Tomates concassées", False), (28, "Oignons", False), (29, "Épices chili", False)],
#     8: [(30, "Haricots blancs", False), (31, "Confit de canard", False), (32, "Saucisse de Toulouse", False), (33, "Porc", False)],
#     9: [(34, "Potimarron", False), (12, "Ail", False), (35, "Crème fraîche", False), (36, "Oignon", False)],
#     10: [(31, "Confit de canard", False), (7, "Pommes de terre", False), (37, "Beurre", False), (38, "Lait", False)],
#     11: [(39, "Fromage à raclette", True), (7, "Pommes de terre", False), (40, "Charcuterie variée", False), (41, "Cornichons", False)]
# }

# # Insertion des ingrédients (unique globalement)
# all_ingredients = set()
# for ingr_list in ingredients_dict.values():
#     for ing in ingr_list:
#         all_ingredients.add(ing)

# for ing in all_ingredients:
#     cursor.execute("INSERT OR IGNORE INTO Ingredients (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)", ing)

# # Quantités pour chaque recette (Recette_id, Id_ingredient, Valeur, Unite)
# quantities_dict = {
#     2: [(2, 6, 1, "chou"), (2, 7, 800, "grammes"), (2, 8, 300, "grammes"), (2, 9, 200, "grammes"), (2, 10, 3, "unités")],
#     3: [(3, 7, 800, "grammes"), (3, 11, 300, "ml"), (3, 12, 2, "gousses"), (3, 13, 30, "grammes")],
#     4: [(4, 14, 5, "unités"), (4, 15, 1, "litre"), (4, 16, 150, "grammes"), (4, 17, 4, "tranches")],
#     5: [(5, 18, 1.5, "kg"), (5, 19, 750, "ml"), (5, 20, 4, "unités"), (5, 21, 300, "grammes"), (5, 22, 2, "unités")],
#     6: [(6, 7, 1, "kg"), (6, 23, 450, "grammes"), (6, 24, 150, "grammes"), (6, 22, 1, "unité")],
#     7: [(7, 25, 600, "grammes"), (7, 26, 400, "grammes"), (7, 27, 500, "grammes"), (7, 28, 1, "unité"), (7, 29, 1, "cuillère à soupe")],
#     8: [(8, 30, 500, "grammes"), (8, 31, 600, "grammes"), (8, 32, 400, "grammes"), (8, 33, 300, "grammes")],
#     9: [(9, 34, 1, "kg"), (9, 12, 1, "gousse"), (9, 35, 200, "ml"), (9, 36, 1, "unité")],
#     10: [(10, 31, 600, "grammes"), (10, 7, 800, "grammes"), (10, 37, 50, "grammes"), (10, 38, 100, "ml")],
#     11: [(11, 39, 600, "grammes"), (11, 7, 1, "kg"), (11, 40, 300, "grammes"), (11, 41, 100, "grammes")]
# }

# for rid, quants in quantities_dict.items():
#     for q in quants:
#         cursor.execute("""
#         INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
#         VALUES (?, ?, ?, ?)
#         """, q)

# # Equipement (matériel) pour chaque recette
# equipment_dict = {
#     2: [(4, "Cocotte", 2), (5, "Couteau", 2), (6, "Planche à découper", 2)],
#     3: [(7, "Plat à gratin", 3), (8, "Couteau", 3), (9, "Four", 3)],
#     4: [(10, "Casserole", 4), (11, "Gril du four", 4), (12, "Couteau", 4)],
#     5: [(13, "Cocotte", 5), (14, "Couteau", 5), (15, "Planche à découper", 5)],
#     6: [(16, "Plat à gratin", 6), (17, "Couteau", 6), (18, "Poêle", 6)],
#     7: [(19, "Casserole", 7), (20, "Cuillère en bois", 7), (21, "Couteau", 7)],
#     8: [(22, "Cocotte", 8), (23, "Couteau", 8), (24, "Planche à découper", 8)],
#     9: [(25, "Casserole", 9), (26, "Mixeur", 9), (27, "Couteau", 9)],
#     10: [(28, "Plat à gratin", 10), (29, "Four", 10), (30, "Couteau", 10)],
#     11: [(31, "Appareil à raclette", 11), (32, "Couteau", 11), (33, "Fourchette", 11)]
# }

# for eq_list in equipment_dict.values():
#     for eq in eq_list:
#         cursor.execute("INSERT INTO Equipment (Id_equipement, Name) VALUES (?, ?, ?)", eq)


# ## PLATS ETE

# recettes_ete = [
#     (12, "Salade niçoise", 20, 0, "Plat", "Été",
#      "Salade méditerranéenne composée de légumes frais, thon et œufs durs.", 4, "salade_nicoise.jpg"),
#     (13, "Taboulé libanais", 15, 0, "Entrée", "Été",
#      "Salade fraîche à base de boulgour, persil, tomates et citron.", 4, "taboule.jpg"),
#     (14, "Tian de légumes", 20, 60, "Plat", "Été",
#      "Gratin de légumes méditerranéens en fines tranches, parfumé aux herbes.", 4, "tian_legumes.jpg"),
#     (15, "Brochettes de poulet marinées", 25, 15, "Plat", "Été",
#      "Brochettes grillées de poulet marinées au citron et aux herbes.", 4, "brochettes_poulet.jpg"),
#     (16, "Gaspacho andalou", 15, 0, "Entrée", "Été",
#      "Soupe froide de légumes frais mixés, idéale pour se rafraîchir.", 4, "gaspacho.jpg"),
#     (17, "Ratatouille", 20, 50, "Plat", "Été",
#      "Mijoté de légumes provençaux parfumé au thym et au basilic.", 6, "ratatouille.jpg"),
#     (18, "Poke bowl au saumon", 20, 0, "Plat", "Été",
#      "Bol coloré avec saumon cru mariné, riz, légumes croquants et algues.", 2, "poke_bowl.jpg"),
#     (19, "Quiche aux légumes d'été", 25, 35, "Plat", "Été",
#      "Quiche légère aux courgettes, tomates et poivrons.", 6, "quiche_legumes.jpg"),
#     (20, "Salade de pâtes méditerranéenne", 15, 10, "Plat", "Été",
#      "Salade froide de pâtes, olives, tomates séchées et mozzarella.", 4, "salade_pates.jpg"),
#     (21, "Pizza Margherita maison", 30, 15, "Plat", "Été",
#      "Pizza fine et fraîche à la tomate, mozzarella et basilic.", 4, "pizza_margherita.jpg"),
# ]

# for r in recettes_ete:
#     cursor.execute("""
#     INSERT INTO Recettes (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, r)

# steps_ete = {
#     12: [
#         "Faites cuire les œufs et laissez-les refroidir.",
#         "Coupez tomates, poivrons, olives et haricots verts.",
#         "Disposez les légumes, œufs coupés et thon dans un plat.",
#         "Assaisonnez avec huile d'olive, vinaigre, sel et poivre.",
#         "Servez frais."
#     ],
#     13: [
#         "Faites tremper le boulgour dans de l'eau froide pendant 15 minutes.",
#         "Hachez finement persil, menthe et oignon.",
#         "Mélangez boulgour égoutté, herbes, tomates et jus de citron.",
#         "Assaisonnez d'huile d'olive, sel et poivre.",
#         "Réfrigérez avant de servir."
#     ],
#     14: [
#         "Coupez les légumes en fines rondelles.",
#         "Disposez-les en couches alternées dans un plat à gratin.",
#         "Arrosez d'huile d'olive et parsemez d'herbes de Provence.",
#         "Cuisez au four à 180°C pendant 1 heure.",
#         "Servez chaud ou tiède."
#     ],
#     15: [
#         "Préparez une marinade avec citron, ail, huile d'olive et herbes.",
#         "Coupez le poulet en cubes et laissez mariner 20 minutes.",
#         "Enfilez les cubes de poulet sur des brochettes.",
#         "Faites griller au barbecue ou à la poêle 15 minutes.",
#         "Servez avec une salade verte."
#     ],
#     16: [
#         "Coupez tomates, concombre, poivron et oignon.",
#         "Mixez tous les légumes avec du pain rassis, huile d'olive et vinaigre.",
#         "Salez, poivrez et réfrigérez pendant au moins 2 heures.",
#         "Servez très frais."
#     ],
#     17: [
#         "Coupez tous les légumes en dés.",
#         "Faites revenir oignons et ail dans de l'huile d'olive.",
#         "Ajoutez les légumes et laissez mijoter 45 minutes.",
#         "Assaisonnez avec thym, laurier et basilic.",
#         "Servez chaud."
#     ],
#     18: [
#         "Cuisez le riz et laissez-le refroidir.",
#         "Préparez une marinade soja, citron et gingembre pour le saumon.",
#         "Coupez le saumon en dés et faites mariner 10 minutes.",
#         "Disposez riz, saumon et légumes dans un bol.",
#         "Ajoutez graines de sésame et sauce soja."
#     ],
#     19: [
#         "Préparez une pâte brisée ou achetez-la prête.",
#         "Coupez légumes en petits morceaux et faites-les revenir.",
#         "Étalez la pâte dans un moule, ajoutez légumes et mélange œufs-crème.",
#         "Cuisez au four à 180°C pendant 35 minutes.",
#         "Laissez tiédir avant de servir."
#     ],
#     20: [
#         "Faites cuire les pâtes, égouttez et laissez refroidir.",
#         "Coupez tomates séchées, olives et mozzarella.",
#         "Mélangez tous les ingrédients avec de l'huile d'olive.",
#         "Assaisonnez sel, poivre et herbes fraîches.",
#         "Servez frais."
#     ],
#     21: [
#         "Préparez la pâte à pizza et étalez-la finement.",
#         "Étalez la sauce tomate puis ajoutez tranches de mozzarella.",
#         "Cuisez au four à 220°C pendant 12-15 minutes.",
#         "Parsemez de feuilles de basilic frais.",
#         "Servez chaud."
#     ],
# }

# for rid, steps in steps_ete.items():
#     for i, contenu in enumerate(steps, start=1):
#         cursor.execute("""
#         INSERT INTO Steps (Recette_id, Num_step, Contenu)
#         VALUES (?, ?, ?)
#         """, (rid, i, contenu))

# ingredients_ete = {
#     12: [(42, "Œufs", False), (43, "Tomates", False), (44, "Haricots verts", False), (45, "Olives noires", False), (46, "Thon en boîte", False), (47, "Poivron", False)],
#     13: [(48, "Boulgour", False), (49, "Persil", False), (50, "Menthe", False), (43, "Tomates", False), (51, "Citron", False), (52, "Oignon", False)],
#     14: [(43, "Tomates", False), (53, "Courgettes", False), (54, "Aubergines", False), (55, "Herbes de Provence", False), (56, "Huile d'olive", False)],
#     15: [(57, "Poulet", False), (51, "Citron", False), (58, "Ail", False), (56, "Huile d'olive", False), (59, "Herbes fraîches", False)],
#     16: [(43, "Tomates", False), (60, "Concombre", False), (47, "Poivron", False), (52, "Oignon", False), (61, "Pain rassis", False), (56, "Huile d'olive", False)],
#     17: [(52, "Oignon", False), (58, "Ail", False), (53, "Courgettes", False), (54, "Aubergines", False), (43, "Tomates", False), (62, "Thym", False), (63, "Laurier", False), (64, "Basilic", False)],
#     18: [(65, "Riz", False), (66, "Saumon frais", False), (67, "Sauce soja", False), (51, "Citron", False), (68, "Gingembre", False), (69, "Graines de sésame", False), (70, "Légumes croquants", False)],
#     19: [(71, "Pâte brisée", False), (53, "Courgettes", False), (43, "Tomates", False), (47, "Poivron", False), (72, "Œufs", False), (73, "Crème fraîche", False)],
#     20: [(74, "Pâtes", False), (45, "Olives noires", False), (43, "Tomates séchées", False), (75, "Mozzarella", True), (56, "Huile d'olive", False)],
#     21: [(76, "Pâte à pizza", False), (77, "Sauce tomate", False), (75, "Mozzarella", True), (78, "Basilic frais", False)],
# }

# # Insertion des ingrédients (éviter doublons avec INSERT OR IGNORE)
# all_ingredients_ete = set()
# for ingr_list in ingredients_ete.values():
#     for ing in ingr_list:
#         all_ingredients_ete.add(ing)

# for ing in all_ingredients_ete:
#     cursor.execute("INSERT OR IGNORE INTO Ingredients (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)", ing)

# quantities_ete = {
#     12: [(12, 42, 4, "unités"), (12, 43, 4, "unités"), (12, 44, 150, "grammes"), (12, 45, 50, "grammes"), (12, 46, 1, "boîte"), (12, 47, 1, "unité")],
#     13: [(13, 48, 200, "grammes"), (13, 49, 50, "grammes"), (13, 50, 30, "grammes"), (13, 43, 3, "unités"), (13, 51, 1, "unité"), (13, 52, 1, "unité")],
#     14: [(14, 43, 3, "unités"), (14, 53, 2, "unités"), (14, 54, 2, "unités"), (14, 55, 1, "cuillère à soupe"), (14, 56, 3, "cuillères à soupe")],
#     15: [(15, 57, 600, "grammes"), (15, 51, 1, "unité"), (15, 58, 2, "gousses"), (15, 56, 3, "cuillères à soupe"), (15, 59, 1, "cuillère à soupe")],
#     16: [(16, 43, 5, "unités"), (16, 60, 1, "unité"), (16, 47, 1, "unité"), (16, 52, 1, "unité"), (16, 61, 50, "grammes"), (16, 56, 3, "cuillères à soupe")],
#     17: [(17, 52, 1, "unité"), (17, 58, 2, "gousses"), (17, 53, 2, "unités"), (17, 54, 2, "unités"), (17, 43, 4, "unités"), (17, 62, 1, "cuillère à café"), (17, 63, 2, "feuilles"), (17, 64, 5, "feuilles")],
#     18: [(18, 65, 200, "grammes"), (18, 66, 200, "grammes"), (18, 67, 3, "cuillères à soupe"), (18, 51, 1, "unité"), (18, 68, 1, "cuillère à café"), (18, 69, 1, "cuillère à soupe"), (18, 70, 150, "grammes")],
#     19: [(19, 71, 1, "pâte"), (19, 53, 2, "unités"), (19, 43, 3, "unités"), (19, 47, 1, "unité"), (19, 72, 3, "unités"), (19, 73, 200, "ml")],
#     20: [(20, 74, 300, "grammes"), (20, 45, 50, "grammes"), (20, 43, 100, "grammes"), (20, 75, 150, "grammes"), (20, 56, 3, "cuillères à soupe")],
#     21: [(21, 76, 1, "pâte"), (21, 77, 150, "grammes"), (21, 75, 150, "grammes"), (21, 78, 10, "feuilles")],
# }

# for rid, quants in quantities_ete.items():
#     for q in quants:
#         cursor.execute("""
#         INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
#         VALUES (?, ?, ?, ?)
#         """, q)

# equipment_ete = {
#     12: [(34, "Casserole", 12), (35, "Saladier", 12), (36, "Cuillère", 12)],
#     13: [(37, "Bol", 13), (38, "Couteau", 13), (39, "Planche à découper", 13)],
#     14: [(40, "Plat à gratin", 14), (41, "Couteau", 14), (42, "Four", 14)],
#     15: [(43, "Brochettes", 15), (44, "Barbecue", 15), (45, "Bol", 15)],
#     16: [(34, "Mixeur", 16), (46, "Saladier", 16)],
#     17: [(40, "Casserole", 17), (41, "Cuillère en bois", 17)],
#     18: [(47, "Bol", 18), (48, "Couteau", 18)],
#     19: [(49, "Moule à tarte", 19), (50, "Four", 19), (51, "Fouet", 19)],
#     20: [(52, "Saladier", 20), (53, "Couteau", 20)],
#     21: [(54, "Four", 21), (55, "Plaque de cuisson", 21)],
# }

# for rid, eqs in equipment_ete.items():
#     for eq_id, eq_name, rec_id in eqs:
#         cursor.execute("""
#         INSERT OR IGNORE INTO Equipment (Id_equipment, Name)
#         VALUES (?, ?)
#         """, (eq_id, eq_name))
#         cursor.execute("""
#         INSERT INTO LinkEquipment (Id_equipment, Recette_id)
#         VALUES (?, ?)
#         """, (eq_id, rec_id))
        
# ## PLATS PRINTEMPS

# recettes_printemps = [
#     (22, "Asperges vertes rôties au parmesan", 15, 15, "Entrée", "Printemps",
#      "Asperges vertes rôties au four avec du parmesan gratiné.", 4, "asperges_parmesan.jpg"),
#     (23, "Tarte aux légumes de printemps", 30, 40, "Plat", "Printemps",
#      "Tarte salée garnie de légumes frais comme petits pois, carottes et fèves.", 6, "tarte_printemps.jpg"),
#     (24, "Salade de radis, concombre et fromage frais", 15, 0, "Entrée", "Printemps",
#      "Salade croquante et légère avec radis, concombre et fromage frais.", 4, "salade_radis.jpg"),
#     (25, "Poulet aux morilles et petits légumes", 25, 45, "Plat", "Printemps",
#      "Poulet mijoté avec morilles et légumes printaniers.", 4, "poulet_morilles.jpg"),
#     (26, "Velouté d’orties", 20, 30, "Entrée", "Printemps",
#      "Soupe douce et nutritive à base d’orties fraîches.", 4, "veloute_orties.jpg"),
#     (27, "Quiche aux asperges et saumon fumé", 30, 35, "Plat", "Printemps",
#      "Quiche légère aux asperges vertes et saumon fumé.", 6, "quiche_asperges.jpg"),
#     (28, "Risotto aux petits pois et menthe", 20, 30, "Plat", "Printemps",
#      "Risotto crémeux aux petits pois et une touche de menthe fraîche.", 4, "risotto_petits_pois.jpg"),
#     (29, "Omelette aux fines herbes et champignons", 10, 15, "Plat", "Printemps",
#      "Omelette légère avec herbes fraîches et champignons sautés.", 2, "omelette_herbes.jpg"),
#     (30, "Salade de fraises, épinards et chèvre frais", 10, 0, "Entrée", "Printemps",
#      "Salade sucrée-salée avec fraises, épinards et fromage de chèvre.", 4, "salade_fraises.jpg"),
#     (31, "Filet de poisson à la sauce citronnée et asperges", 20, 20, "Plat", "Printemps",
#      "Filet de poisson blanc servi avec une sauce au citron et asperges vapeur.", 4, "poisson_asperges.jpg"),
# ]

# for r in recettes_printemps:
#     cursor.execute("""
#     INSERT INTO Recettes (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, r)

# steps_printemps = {
#     22: [
#         "Préchauffez le four à 200°C.",
#         "Lavez et coupez les asperges en morceaux.",
#         "Disposez-les sur une plaque, arrosez d’huile d’olive et parsemez de parmesan.",
#         "Faites rôtir 15 minutes.",
#         "Servez chaud."
#     ],
#     23: [
#         "Préparez une pâte brisée.",
#         "Faites cuire à la vapeur petits pois, carottes et fèves.",
#         "Étalez la pâte dans un moule, disposez les légumes.",
#         "Versez un mélange œufs-crème et assaisonnez.",
#         "Cuisez au four à 180°C pendant 40 minutes."
#     ],
#     24: [
#         "Lavez et coupez radis et concombre en rondelles.",
#         "Mélangez avec le fromage frais et un filet d’huile d’olive.",
#         "Assaisonnez sel, poivre et ciboulette.",
#         "Servez frais."
#     ],
#     25: [
#         "Faites revenir le poulet dans une cocotte.",
#         "Ajoutez les morilles et les légumes coupés.",
#         "Couvrez d’eau ou bouillon, laissez mijoter 45 minutes.",
#         "Salez, poivrez et servez chaud."
#     ],
#     26: [
#         "Lavez soigneusement les orties avec des gants.",
#         "Faites revenir oignon et pommes de terre.",
#         "Ajoutez les orties et bouillon, laissez cuire 20 minutes.",
#         "Mixez en velouté, rectifiez l’assaisonnement.",
#         "Servez chaud."
#     ],
#     27: [
#         "Préparez la pâte brisée dans un moule.",
#         "Faites blanchir les asperges 5 minutes.",
#         "Disposez asperges et saumon fumé sur la pâte.",
#         "Versez un mélange œufs-crème, assaisonnez.",
#         "Cuisez 35 minutes à 180°C."
#     ],
#     28: [
#         "Faites revenir l’oignon dans une casserole.",
#         "Ajoutez le riz et mouillez petit à petit avec le bouillon.",
#         "Incorporez les petits pois à mi-cuisson.",
#         "Ajoutez menthe ciselée à la fin.",
#         "Servez chaud."
#     ],
#     29: [
#         "Battez les œufs avec sel, poivre et herbes fines.",
#         "Faites revenir les champignons.",
#         "Versez les œufs dans la poêle, ajoutez les champignons.",
#         "Cuisez doucement et servez."
#     ],
#     30: [
#         "Lavez les épinards et les fraises.",
#         "Mélangez épinards, fraises coupées et chèvre émietté.",
#         "Assaisonnez d’huile d’olive, sel et poivre.",
#         "Servez frais."
#     ],
#     31: [
#         "Faites cuire les filets de poisson à la poêle.",
#         "Faites cuire les asperges à la vapeur.",
#         "Préparez une sauce citronnée avec jus de citron, beurre et persil.",
#         "Servez le poisson nappé de sauce avec les asperges."
#     ],
# }

# for rid, steps in steps_printemps.items():
#     for i, contenu in enumerate(steps, start=1):
#         cursor.execute("""
#         INSERT INTO Steps (Recette_id, Num_step, Contenu)
#         VALUES (?, ?, ?)
#         """, (rid, i, contenu))

# ingredients_printemps = {
#     22: [(79, "Asperges vertes", False), (80, "Parmesan râpé", True), (56, "Huile d'olive", False)],
#     23: [(71, "Pâte brisée", False), (81, "Petits pois", False), (82, "Carottes", False), (83, "Fèves", False), (72, "Œufs", False), (73, "Crème fraîche", False)],
#     24: [(84, "Radis", False), (60, "Concombre", False), (85, "Fromage frais", True), (56, "Huile d'olive", False), (86, "Ciboulette", False)],
#     25: [(87, "Poulet", False), (88, "Morilles", False), (89, "Carottes", False), (90, "Oignon", False), (91, "Bouillon de volaille", False)],
#     26: [(92, "Orties fraîches", False), (90, "Oignon", False), (93, "Pommes de terre", False), (94, "Bouillon de légumes", False)],
#     27: [(71, "Pâte brisée", False), (79, "Asperges vertes", False), (95, "Saumon fumé", False), (72, "Œufs", False), (73, "Crème fraîche", False)],
#     28: [(96, "Riz Arborio", False), (97, "Oignon", False), (81, "Petits pois", False), (98, "Menthe fraîche", False), (99, "Bouillon de légumes", False)],
#     29: [(72, "Œufs", False), (100, "Herbes fines (persil, ciboulette)", False), (101, "Champignons", False)],
#     30: [(102, "Épinards frais", False), (103, "Fraises", False), (104, "Chèvre frais", True), (56, "Huile d'olive", False)],
#     31: [(105, "Filet de poisson blanc", False), (79, "Asperges vertes", False), (106, "Citron", False), (56, "Beurre", False), (107, "Persil", False)],
# }

# all_ingredients_printemps = set()
# for ingr_list in ingredients_printemps.values():
#     for ing in ingr_list:
#         all_ingredients_printemps.add(ing)

# for ing in all_ingredients_printemps:
#     cursor.execute("INSERT OR IGNORE INTO Ingredients (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)", ing)

# quantities_printemps = {
#     22: [(22, 79, 500, "grammes"), (22, 80, 50, "grammes"), (22, 56, 2, "cuillères à soupe")],
#     23: [(23, 71, 1, "pâte"), (23, 81, 200, "grammes"), (23, 82, 150, "grammes"), (23, 83, 150, "grammes"), (23, 72, 3, "unités"), (23, 73, 200, "ml")],
#     24: [(24, 84, 150, "grammes"), (24, 60, 1, "unité"), (24, 85, 150, "grammes"), (24, 56, 2, "cuillères à soupe"), (24, 86, 10, "grammes")],
#     25: [(25, 87, 600, "grammes"), (25, 88, 200, "grammes"), (25, 89, 150, "grammes"), (25, 90, 1, "unité"), (25, 91, 500, "ml")],
#     26: [(26, 92, 200, "grammes"), (26, 90, 1, "unité"), (26, 93, 200, "grammes"), (26, 94, 500, "ml")],
#     27: [(27, 71, 1, "pâte"), (27, 79, 300, "grammes"), (27, 95, 150, "grammes"), (27, 72, 3, "unités"), (27, 73, 200, "ml")],
#     28: [(28, 96, 200, "grammes"), (28, 97, 1, "unité"), (28, 81, 150, "grammes"), (28, 98, 10, "grammes"), (28, 99, 500, "ml")],
#     29: [(29, 72, 3, "unités"), (29, 100, 10, "grammes"), (29, 101, 150, "grammes")],
#     30: [(30, 102, 150, "grammes"), (30, 103, 200, "grammes"), (30, 104, 150, "grammes"), (30, 56, 2, "cuillères à soupe")],
#     31: [(31, 105, 600, "grammes"), (31, 79, 300, "grammes"), (31, 106, 1, "unité"), (31, 56, 30, "grammes"), (31, 107, 5, "grammes")],
# }

# for rid, quants in quantities_printemps.items():
#     for q in quants:
#         cursor.execute("""
#         INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
#         VALUES (?, ?, ?, ?)
#         """, q)

# equipment_printemps = {
#     22: [(56, "Plaque de cuisson", 22), (57, "Four", 22)],
#     23: [(58, "Moule à tarte", 23), (57, "Four", 23)],
#     24: [(59, "Saladier", 24), (60, "Couteau", 24)],
#     25: [(61, "Cocotte", 25), (62, "Couteau", 25)],
#     26: [(63, "Mixeur", 26), (64, "Casserole", 26)],
#     27: [(58, "Moule à tarte", 27), (57, "Four", 27)],
#     28: [(65, "Casserole", 28), (66, "Cuillère en bois", 28)],
#     29: [(67, "Poêle", 29), (68, "Fouet", 29)],
#     30: [(69, "Saladier", 30), (60, "Couteau", 30)],
#     31: [(70, "Poêle", 31), (71, "Vapeur", 31)],
# }

# for rid, eqs in equipment_printemps.items():
#     for eq_id, eq_name, rec_id in eqs:
#         cursor.execute("INSERT OR IGNORE INTO Equipment (Id_equipment, Name) VALUES (?, ?)", (eq_id, eq_name))
#         cursor.execute("INSERT INTO LinkEquipment (Id_equipment, Recette_id) VALUES (?, ?)", (eq_id, rec_id))

#     ## PLATS AUTOMNE

# recettes_automne = [
#     (32, "Risotto aux champignons", 20, 30, "Plat", "Automne",
#      "Un risotto crémeux aux champignons forestiers, relevé au parmesan.", 4, "risotto_champignons.jpg"),
#     (33, "Velouté de potiron", 15, 40, "Entrée", "Automne",
#      "Soupe onctueuse de potiron, relevée avec une pointe de crème.", 4, "veloute_potiron.jpg"),
#     (34, "Tarte aux poireaux", 25, 35, "Plat", "Automne",
#      "Tarte salée garnie de fondue de poireaux et crème fraîche.", 4, "tarte_poireaux.jpg"),
#     (35, "Civet de sanglier", 45, 180, "Plat", "Automne",
#      "Plat mijoté de sanglier mariné au vin rouge et aromates.", 6, "civet_sanglier.jpg"),
#     (36, "Gratin de courge butternut", 20, 45, "Plat", "Automne",
#      "Gratin fondant à base de courge butternut, crème et fromage.", 4, "gratin_butternut.jpg"),
#     (37, "Quiche aux champignons et noisettes", 30, 40, "Plat", "Automne",
#      "Quiche originale aux champignons sautés et éclats de noisette.", 4, "quiche_champignons_noisettes.jpg"),
#     (38, "Poêlée de châtaignes et lardons", 15, 25, "Plat", "Automne",
#      "Poêlée rustique à base de châtaignes, lardons et oignons.", 4, "poelee_chataignes.jpg"),
#     (39, "Gratin de macaronis au potiron", 20, 35, "Plat", "Automne",
#      "Macaronis gratinés avec une sauce onctueuse au potiron.", 4, "gratin_macaronis_potiron.jpg"),
#     (40, "Soupe de lentilles corail et carottes", 15, 30, "Entrée", "Automne",
#      "Soupe épaisse à base de lentilles corail et carottes, parfumée au cumin.", 4, "soupe_lentilles_carottes.jpg"),
#     (41, "Filet mignon aux pommes", 25, 60, "Plat", "Automne",
#      "Filet mignon de porc rôti, accompagné de pommes caramélisées.", 4, "filet_mignon_pommes.jpg"),
# ]

# for r in recettes_automne:
#     cursor.execute("""
#     INSERT INTO Recettes (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, r)

# # Étapes
# steps_dict = {
#     32: [
#         "Faites revenir les champignons émincés dans du beurre.",
#         "Ajoutez le riz et nacrez-le.",
#         "Versez progressivement le bouillon en remuant.",
#         "Incorporez le parmesan en fin de cuisson.",
#         "Servez chaud et crémeux."
#     ],
#     33: [
#         "Épluchez et coupez le potiron en dés.",
#         "Faites revenir l’oignon dans un peu d’huile.",
#         "Ajoutez le potiron et couvrez d’eau.",
#         "Laissez cuire 30 minutes puis mixez.",
#         "Ajoutez la crème et assaisonnez."
#     ],
#     34: [
#         "Lavez et émincez les poireaux.",
#         "Faites-les revenir dans du beurre jusqu’à ce qu’ils fondent.",
#         "Battez œufs et crème, salez, poivrez.",
#         "Garnissez une pâte brisée avec poireaux et appareil.",
#         "Enfournez 35 min à 180°C."
#     ],
#     35: [
#         "Faites mariner la viande avec vin rouge, carottes, oignons et thym pendant 12h.",
#         "Égouttez, puis faites revenir la viande.",
#         "Ajoutez la marinade filtrée et laissez mijoter 3h.",
#         "Ajoutez les champignons en fin de cuisson.",
#         "Servez bien chaud avec des pâtes fraîches."
#     ],
#     36: [
#         "Pelez et coupez la courge en dés.",
#         "Faites-la cuire à l’eau puis égouttez.",
#         "Mélangez avec crème, fromage râpé, sel, poivre.",
#         "Versez dans un plat à gratin et enfournez 45 min.",
#         "Servez doré et chaud."
#     ],
#     37: [
#         "Nettoyez et émincez les champignons.",
#         "Faites-les revenir avec les oignons.",
#         "Concassez les noisettes grossièrement.",
#         "Garnissez une pâte avec champignons, noisettes et appareil œufs/crème.",
#         "Enfournez 40 min à 180°C."
#     ],
#     38: [
#         "Faites revenir les lardons et oignons dans une poêle.",
#         "Ajoutez les châtaignes et laissez dorer.",
#         "Assaisonnez avec poivre et herbes de Provence.",
#         "Servez chaud en accompagnement ou plat principal."
#     ],
#     39: [
#         "Faites cuire les macaronis.",
#         "Faites revenir le potiron en dés dans une casserole.",
#         "Ajoutez crème et épices, mixez en purée.",
#         "Mélangez avec les pâtes, versez dans un plat.",
#         "Ajoutez fromage râpé et gratinez 20 min."
#     ],
#     40: [
#         "Faites revenir un oignon émincé.",
#         "Ajoutez les carottes en rondelles et les lentilles.",
#         "Couvrez d’eau et assaisonnez.",
#         "Laissez cuire 30 min à feu doux.",
#         "Mixez selon la texture souhaitée."
#     ],
#     41: [
#         "Faites revenir le filet mignon dans du beurre.",
#         "Ajoutez les pommes épluchées et coupées en quartiers.",
#         "Versez un peu de cidre ou d’eau pour la cuisson.",
#         "Laissez mijoter 40 min à feu doux.",
#         "Servez nappé de sauce aux pommes."
#     ]
# }

# for rid, steps in steps_dict.items():
#     for i, contenu in enumerate(steps, start=1):
#         cursor.execute("""
#         INSERT INTO Steps (Recette_id, Num_step, Contenu)
#         VALUES (?, ?, ?)
#         """, (rid, i, contenu))

# # Ingrédients
# ingredients_dict = {
#     32: [(50, "Champignons", False), (51, "Riz arborio", False), (52, "Bouillon de légumes", False), (53, "Parmesan", True)],
#     33: [(54, "Potiron", False), (36, "Oignon", False), (35, "Crème fraîche", False)],
#     34: [(55, "Poireaux", False), (56, "Pâte brisée", False), (57, "Œufs", True), (35, "Crème fraîche", False)],
#     35: [(58, "Sanglier", False), (19, "Vin rouge", False), (20, "Carottes", False), (22, "Oignons", False), (21, "Champignons", False)],
#     36: [(59, "Courge butternut", False), (35, "Crème fraîche", False), (60, "Fromage râpé", True)],
#     37: [(50, "Champignons", False), (22, "Oignons", False), (61, "Noisettes", True), (57, "Œufs", True), (35, "Crème fraîche", False)],
#     38: [(62, "Châtaignes", False), (24, "Lardons", False), (22, "Oignons", False)],
#     39: [(63, "Macaronis", False), (54, "Potiron", False), (35, "Crème fraîche", False), (60, "Fromage râpé", True)],
#     40: [(64, "Lentilles corail", False), (20, "Carottes", False), (36, "Oignon", False), (65, "Cumin", False)],
#     41: [(66, "Filet mignon", False), (67, "Pommes", False), (68, "Cidre", False)]
# }

# # Insertion unique
# all_ingredients = set()
# for ingr_list in ingredients_dict.values():
#     for ing in ingr_list:
#         all_ingredients.add(ing)

# for ing in all_ingredients:
#     cursor.execute("INSERT OR IGNORE INTO Ingredients (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)", ing)

# # Quantités
# quantities_dict = {
#     32: [(32, 50, 300, "grammes"), (32, 51, 200, "grammes"), (32, 52, 750, "ml"), (32, 53, 50, "grammes")],
#     33: [(33, 54, 1, "kg"), (33, 36, 1, "unité"), (33, 35, 100, "ml")],
#     34: [(34, 55, 3, "poireaux"), (34, 56, 1, "pâte"), (34, 57, 3, "unités"), (34, 35, 200, "ml")],
#     35: [(35, 58, 1.2, "kg"), (35, 19, 750, "ml"), (35, 20, 3, "unités"), (35, 22, 2, "unités"), (35, 21, 300, "grammes")],
#     36: [(36, 59, 1, "kg"), (36, 35, 200, "ml"), (36, 60, 100, "grammes")],
#     37: [(37, 50, 300, "grammes"), (37, 22, 1, "unité"), (37, 61, 50, "grammes"), (37, 57, 2, "unités"), (37, 35, 150, "ml")],
#     38: [(38, 62, 400, "grammes"), (38, 24, 150, "grammes"), (38, 22, 1, "unité")],
#     39: [(39, 63, 250, "grammes"), (39, 54, 300, "grammes"), (39, 35, 200, "ml"), (39, 60, 100, "grammes")],
#     40: [(40, 64, 200, "grammes"), (40, 20, 3, "unités"), (40, 36, 1, "unité"), (40, 65, 1, "cuillère à café")],
#     41: [(41, 66, 600, "grammes"), (41, 67, 3, "unités"), (41, 68, 200, "ml")]
# }

# for rid, quants in quantities_dict.items():
#     for q in quants:
#         cursor.execute("""
#         INSERT INTO Quantity (Recette_id, Id_ingredient, Valeur, Unite)
#         VALUES (?, ?, ?, ?)
#         """, q)

# # Équipements
# equipment_dict = {
#     32: [(100, "Poêle", 32), (101, "Casserole", 32), (102, "Cuillère en bois", 32)],
#     33: [(103, "Mixeur", 33), (104, "Casserole", 33), (105, "Couteau", 33)],
#     34: [(106, "Four", 34), (107, "Moule à tarte", 34), (108, "Couteau", 34)],
#     35: [(109, "Cocotte", 35), (110, "Couteau", 35), (111, "Passoire", 35)],
#     36: [(112, "Four", 36), (113, "Plat à gratin", 36), (114, "Couteau", 36)],
#     37: [(115, "Poêle", 37), (116, "Four", 37), (117, "Moule à tarte", 37)],
#     38: [(118, "Poêle", 38), (119, "Couteau", 38)],
#     39: [(120, "Casserole", 39), (121, "Four", 39), (122, "Plat à gratin", 39)],
#     40: [(123, "Casserole", 40), (124, "Mixeur", 40), (125, "Couteau", 40)],
#     41: [(126, "Poêle", 41), (127, "Casserole", 41), (128, "Couteau", 41)]
# }

# for eq_list in equipment_dict.values():
#     for eq in eq_list:
#         cursor.execute("INSERT INTO Equipment (Id_equipement, Name) VALUES (?, ?, ?)", eq)

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
        "INSERT OR IGNORE INTO Ingredients (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        INSERT INTO Recettes (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
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
        ""
    ))

    # Ajout étapes
    for num, step in enumerate(dessert["steps"], start=1):
        cursor.execute("""
            INSERT INTO Steps (Recette_id, Num_step, Contenu)
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
            "INSERT OR IGNORE INTO Ingredients (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        INSERT INTO Recettes (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
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
        ""
    ))

    # Ajout étapes
    for num, step in enumerate(dessert["steps"], start=1):
        cursor.execute("""
            INSERT INTO Steps (Recette_id, Num_step, Contenu)
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
            "INSERT OR IGNORE INTO Ingredients (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        INSERT INTO Recettes (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
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
        ""
    ))

    # Ajout étapes
    for num, step in enumerate(dessert["steps"], start=1):
        cursor.execute("""
            INSERT INTO Steps (Recette_id, Num_step, Contenu)
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
                "INSERT OR IGNORE INTO Ingredients (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
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
            "INSERT OR IGNORE INTO Ingredients (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        INSERT INTO Recettes (Recette_id, Title, Preptime, Cooktime, Category, Saison, Description, Servings, Image)
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
        ""
    ))

    # Ajout étapes
    for num, step in enumerate(dessert["steps"], start=1):
        cursor.execute("""
            INSERT INTO Steps (Recette_id, Num_step, Contenu)
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
                "INSERT OR IGNORE INTO Ingredients (Id_ingredient, Name, Allergene) VALUES (?, ?, ?)",
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

# Sauvegarde les changements et ferme la connexion
conn.commit()
conn.close()


