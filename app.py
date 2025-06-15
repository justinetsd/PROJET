from flask import Flask, render_template, request, session, redirect, url_for, flash
import hashlib
import os
import sqlite3
from flask_mail import Mail, Message
import datetime
import random

app = Flask(__name__)
app.secret_key = "votre_cle_secrete"

# Configuration Flask-Mail (exemple avec Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'enacppetit@gmail.com'      # Ton adresse Gmail
app.config['MAIL_PASSWORD'] = 'klqn uabr phum njms'    # Ton mot de passe Gmail ou mot de passe d'application

mail = Mail(app)

def get_recipes():
    conn = sqlite3.connect('BDD.db')
    conn.row_factory = sqlite3.Row
    recipes = conn.execute('SELECT * FROM Recette').fetchall()
    conn.close()
    return recipes

def get_best_rated_recipes(limit=20):
    conn = sqlite3.connect('BDD.db')
    conn.row_factory = sqlite3.Row
    recettes = conn.execute("""
        SELECT r.*, AVG(rt.Rating) as moyenne
        FROM Recette r
        JOIN Rating rt ON r.Recette_id = rt.Recette_id
        GROUP BY r.Recette_id
        HAVING COUNT(rt.Rating) > 0
        ORDER BY moyenne DESC, r.Title ASC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return recettes

@app.route('/') #route par défaut
def accueil():
    recipes = get_recipes()
    best_recipes = get_best_rated_recipes(20)
    return render_template('accueil.html', recipes=recipes, best_recipes=best_recipes)

@app.route('/recettes')
def recettes():
    conn = sqlite3.connect('BDD.db')
    conn.row_factory = sqlite3.Row
    recipes = conn.execute("SELECT * FROM Recette").fetchall()
    plats = [r for r in recipes if r['Category'].lower() == 'plat']
    desserts = [r for r in recipes if r['Category'].lower() == 'dessert']

    today = datetime.date.today().isoformat()
    random.seed(today + "plat")
    plat_du_jour = random.choice(plats) if plats else None
    random.seed(today + "dessert")
    dessert_du_jour = random.choice(desserts) if desserts else None

    conn.close()
    return render_template(
        'recettes.html',
        recipes=recipes,
        plat_du_jour=plat_du_jour,
        dessert_du_jour=dessert_du_jour
    )

@app.route('/recette/<int:recette_id>')
def recette(recette_id):
    conn = sqlite3.connect('BDD.db')
    conn.row_factory = sqlite3.Row
    recipe = conn.execute('SELECT * FROM Recette WHERE Recette_id = ?', (recette_id,)).fetchone()

    if recipe is None:
        conn.close()
        return "Recette non trouvée", 404

    equipements = conn.execute(
        "SELECT Equipment.Name FROM Equipment "
        "JOIN Recette_Equipment ON Equipment.id_equipement = Recette_Equipment.id_equipement "
        "WHERE Recette_Equipment.Recette_id = ?",
        (recette_id,)
    ).fetchall()

    steps = conn.execute(
        "SELECT Num_step,Contenu FROM Step WHERE Recette_id = ? ORDER BY Num_step",
        (recette_id,)
    ).fetchall()

    est_favori = False
    if "username" in session:
        user_id = conn.execute("SELECT User_id FROM User WHERE Username = ?", (session["username"],)).fetchone()
        if user_id:
            user_id = user_id[0]
            fav = conn.execute("SELECT 1 FROM Recette_Favori WHERE User_id = ? AND Recette_id = ?", (user_id, recette_id)).fetchone()
            est_favori = fav is not None
    
    avis = conn.execute(
    "SELECT u.Username, r.Rating, r.Commentaire FROM Rating r JOIN User u ON r.User_id = u.User_id WHERE r.Recette_id = ?",
    (recette_id,)
).fetchall()
    
    moyenne = conn.execute(
    "SELECT AVG(Rating) FROM Rating WHERE Recette_id = ?", (recette_id,)
).fetchone()[0]

    conn.close()
    return render_template('Unerecette.html', recipe=recipe, equipements=equipements, steps=steps, est_favori=est_favori, avis=avis, moyenne=moyenne)


def hashage(password, rand, salt):
    combined = f"{password}{rand}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()

import random

from flask import session

@app.route('/profil')
def profil():
    from flask import session, redirect, url_for
    if not session.get('username'):
        return redirect(url_for('login'))
    conn = sqlite3.connect('BDD.db')
    conn.row_factory = sqlite3.Row
    user = conn.execute("SELECT * FROM User WHERE Username = ?", (session['username'],)).fetchone()
    # Récupère les recettes favorites de l'utilisateur
    favoris = []
    if user:
        favoris = conn.execute("""
            SELECT r.*
            FROM Recette r
            JOIN Recette_Favori f ON r.Recette_id = f.Recette_id
            WHERE f.User_id = ?
        """, (user['User_id'],)).fetchall()
    conn.close()
    if not user:
        return redirect(url_for('login'))
    return render_template(
        'profil.html',
        username=user['Username'],
        firstname=user['FirstName'],
        lastname=user['LastName'],
        favoris=favoris
    )

@app.route('/logout')
def logout():
    from flask import session, redirect, url_for
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    success = None
    if request.method == 'POST':
        nom = request.form['LastName']
        prenom = request.form['FirstName']
        username = request.form['Username']
        email = request.form['EmailAddress']
        password = request.form['password']

        conn = sqlite3.connect('BDD.db')
        c = conn.cursor()

        c.execute("SELECT * FROM User WHERE Username=?", (username,))
        if c.fetchone():
            session['signin_error'] = "Cet identifiant est déjà utilisé."
            conn.close()
            return redirect(url_for('signin'))
        else:
            # Générer un user_id unique à 5 chiffres
            while True:
                user_id = str(random.randint(10000, 99999))
                c.execute("SELECT * FROM User WHERE user_id = ?", (user_id,))
                if not c.fetchone():
                    break
            rand = os.urandom(16).hex()
            salt = os.urandom(16).hex()
            hashed_password = hashage(password, rand, salt)
            c.execute("INSERT INTO User (User_id, Username, FirstName, LastName, EmailAddress, Salt, Random, Hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (user_id, username, prenom, nom, email, salt, rand, hashed_password))
            conn.commit()
            conn.close()
            session['signin_success'] = "Inscription réussie ! Vous pouvez maintenant vous connecter."
            return redirect(url_for('signin'))

    # Ici, on affiche la page en GET (après redirection)
    error = session.pop('signin_error', None)
    success = session.pop('signin_success', None)
    return render_template('signin.html', error=error, success=success)


@app.route('/login', methods=['GET', 'POST']) #route de connexion
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("BDD.db")
        cur = conn.cursor()

        cur.execute("SELECT Random, Salt, Hash FROM User WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()

        if row:
            rand, salt, stored_hash = row
            computed_hash = hashage(password, rand, salt)

            if computed_hash == stored_hash:
                session["username"] = username
                return redirect("/")
        
        return render_template("login.html", error="Identifiant ou mot de passe incorrect.")

    return render_template("login.html")

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    message = None
    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect('BDD.db')
        conn.row_factory = sqlite3.Row  # <-- Ajoute ceci
        user = conn.execute("SELECT * FROM User WHERE EmailAddress = ?", (email,)).fetchone()
        conn.close()
        if user:
            # Génère un token unique (ici simple, à sécuriser en prod)
            import secrets
            token = secrets.token_urlsafe(32)
            # Stocke le token temporairement (à améliorer pour la prod)
            with open(f"reset_{token}.txt", "w") as f:
                f.write(user['Username'])
            # Envoie le mail
            reset_link = url_for('reset_password', token=token, _external=True)
            from flask_mail import Message
            msg = Message(
                "Réinitialisation de votre mot de passe",
                sender=app.config['MAIL_USERNAME'],  # <-- ajoute ceci
                recipients=[email]
            )
            msg.body = f"Pour réinitialiser votre mot de passe, cliquez sur ce lien : {reset_link}"
            mail.send(msg)
            message = "Un email de réinitialisation a été envoyé."
        else:
            message = "Adresse email inconnue."
    return render_template('forgot_password.html', message=message)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    import os
    username_file = f"reset_{token}.txt"
    if not os.path.exists(username_file):
        return "Lien invalide ou expiré.", 400
    with open(username_file, "r") as f:
        username = f.read()
    error = None
    success = None
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if new_password != confirm_password:
            error = "Les mots de passe ne correspondent pas."
        else:
            conn = sqlite3.connect('BDD.db')
            conn.row_factory = sqlite3.Row
            user = conn.execute("SELECT * FROM User WHERE Username = ? AND EmailAddress = ?", (username, email)).fetchone()
            if not user:
                error = "Adresse email incorrecte."
            else:
                salt, rand = user['Salt'], user['Random']
                new_hash = hashage(new_password, rand, salt)
                conn.execute("UPDATE User SET Hash = ? WHERE Username = ?", (new_hash, username))
                conn.commit()
                conn.close()
                os.remove(username_file)
                # Redirige vers la page de connexion avec un message de succès
                return redirect(url_for('login', reset_success=1))
            conn.close()
    # error sera None en GET, ou contiendra le message seulement après un POST
    return render_template('reset_password.html', error=error, method=request.method)

@app.route('/ete')
def ete():
    conn = sqlite3.connect('BDD.db')
    conn.row_factory = sqlite3.Row
    plats = conn.execute("SELECT * FROM Recette WHERE saison = 'Été' AND category = 'Plat'").fetchall()
    desserts = conn.execute("SELECT * FROM Recette WHERE saison = 'Été' AND category = 'Dessert'").fetchall()
    conn.close()
    return render_template('ete.html', plats=plats, desserts=desserts)

@app.route('/automne')
def automne():
    conn = sqlite3.connect('BDD.db')
    conn.row_factory = sqlite3.Row
    plats = conn.execute("SELECT * FROM Recette WHERE saison = 'Automne' AND category = 'Plat'").fetchall()
    desserts = conn.execute("SELECT * FROM Recette WHERE saison = 'Automne' AND category = 'Dessert'").fetchall()
    conn.close()
    return render_template('automne.html', plats=plats, desserts=desserts)

@app.route('/hiver')
def hiver():
    conn = sqlite3.connect('BDD.db')
    conn.row_factory = sqlite3.Row
    plats = conn.execute("SELECT * FROM Recette WHERE saison = 'Hiver' AND category = 'Plat'").fetchall()
    desserts = conn.execute("SELECT * FROM Recette WHERE saison = 'Hiver' AND category = 'Dessert'").fetchall()
    conn.close()
    return render_template('hiver.html', plats=plats, desserts=desserts)

@app.route('/printemps')
def printemps():
    conn = sqlite3.connect('BDD.db')
    conn.row_factory = sqlite3.Row
    plats = conn.execute("SELECT * FROM Recette WHERE saison = 'Printemps' AND category = 'Plat'").fetchall()
    desserts = conn.execute("SELECT * FROM Recette WHERE saison = 'Printemps' AND category = 'Dessert'").fetchall()
    conn.close()
    return render_template('printemps.html', plats=plats, desserts=desserts)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        email = request.form["email"]
        objet = request.form["objet"]
        message = request.form["message"]

        msg = Message(
            subject=f"Contact ENAC'ppetit : {objet}",
            sender=email,
            recipients=["enacppetit@gmail.com"],
            body=f"Adresse mail de l'expéditeur : {email}\n\nObjet : {objet}\n\nMessage :\n{message}"
        )
        mail.send(msg)
        flash("Votre message a bien été envoyé, merci !")
        return redirect(url_for("contact"))
    return render_template("contact.html")


# Configuration Flask-Mail (exemple avec Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'enacppetit@gmail.com'      # Ton adresse Gmail
app.config['MAIL_PASSWORD'] = 'klqn uabr phum njms'    # Ton mot de passe Gmail ou mot de passe d'application

mail = Mail(app)

@app.route('/apropos')
def apropos():
    return render_template('apropos.html')

@app.route('/recherche', methods=['GET'])
def recherche():
    query = request.args.get('q', '')
    recettes = []
    if query:
        ingredients = [i.strip() for i in query.replace(',', ' ').split() if i.strip()]
        conn = sqlite3.connect('BDD.db')
        conn.row_factory = sqlite3.Row
        where = ["r.Title LIKE ?"]
        params = [f"%{query}%"]
        if ingredients:
            where += ["i.Name LIKE ?"] * len(ingredients)
            params += [f"%{ing}%" for ing in ingredients]
        sql = f"""
            SELECT DISTINCT r.*
            FROM Recette r
            LEFT JOIN Quantity q ON r.Recette_id = q.Recette_id
            LEFT JOIN Ingredient i ON q.Id_ingredient = i.Id_ingredient
            WHERE {' OR '.join(where)}
            ORDER BY CASE WHEN r.Title LIKE ? THEN 1 ELSE 2 END, r.Title
        """
        params.append(f"%{query}%")
        recettes = conn.execute(sql, params).fetchall()
        conn.close()
    return render_template('recherche.html', recettes=recettes, query=query)

@app.route('/noter_recette/<int:recette_id>', methods=['POST'])
def noter_recette(recette_id):
    if "username" not in session:
        return redirect(url_for('login'))
    note = int(request.form.get('note', 0))
    commentaire = request.form.get('commentaire', '').strip()
    username = session["username"]
    conn = sqlite3.connect('BDD.db')
    cur = conn.cursor()
    user_id = cur.execute("SELECT User_id FROM User WHERE Username = ?", (username,)).fetchone()
    if user_id:
        user_id = user_id[0]
        cur.execute("""
            INSERT INTO Rating (User_id, Recette_id, Rating, Commentaire)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(User_id, Recette_id) DO UPDATE SET Rating=excluded.Rating, Commentaire=excluded.Commentaire
        """, (user_id, recette_id, note, commentaire))
        conn.commit()
    conn.close()
    flash("Merci pour votre note !")
    return redirect(url_for('recette', recette_id=recette_id))

@app.route('/politique')
def politique():
    return render_template('politique.html')

@app.route('/conditions')
def conditions():
    return render_template('conditions.html')

@app.route('/ajouter_favori/<int:recette_id>', methods=['POST'])
def ajouter_favori(recette_id):
    if "username" not in session:  # <-- correction ici
        return redirect(url_for('login'))
    username = session["username"]
    conn = sqlite3.connect('BDD.db')
    cur = conn.cursor()
    user_id = cur.execute("SELECT User_id FROM User WHERE Username = ?", (username,)).fetchone()
    if user_id:
        user_id = user_id[0]
        cur.execute("INSERT OR IGNORE INTO Recette_Favori (User_id, Recette_id) VALUES (?, ?)", (user_id, recette_id))
        conn.commit()
    conn.close()
    return redirect(url_for('recette', recette_id=recette_id))

@app.route('/retirer_favori/<int:recette_id>', methods=['POST'])
def retirer_favori(recette_id):
    if "username" not in session:
        return redirect(url_for('login'))
    username = session["username"]
    conn = sqlite3.connect('BDD.db')
    cur = conn.cursor()
    user_id = cur.execute("SELECT User_id FROM User WHERE Username = ?", (username,)).fetchone()
    if user_id:
        user_id = user_id[0]
        cur.execute("DELETE FROM Recette_Favori WHERE User_id = ? AND Recette_id = ?", (user_id, recette_id))
        conn.commit()
    conn.close()
    return redirect(url_for('recette', recette_id=recette_id))

if __name__ == '__main__':
    app.run(debug=True)


