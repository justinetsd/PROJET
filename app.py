from flask import Flask, render_template, request, session, redirect, url_for, flash
import hashlib
import os
import sqlite3
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "votre_cle_secrete"

# Configuration Flask-Mail (exemple avec Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'enacppetit@gmail.com'      # Ton adresse Gmail
app.config['MAIL_PASSWORD'] = 'klqn uabr phum njms'    # Ton mot de passe Gmail ou mot de passe d'application

mail = Mail(app)

def get_recipes(): #recette
    conn = sqlite3.connect('BDD.db')
    
    conn.row_factory = sqlite3.Row
    recipes = conn.execute('SELECT * FROM Recette').fetchall()
    conn.close()
    return recipes

@app.route('/') #route par défaut
def accueil():
    recipes = get_recipes()
    return render_template('accueil.html', recipes=recipes)

@app.route('/recettes') #route des recettes
def recettes():
    recipes = get_recipes()
    return render_template('recettes.html', recipes=recipes)
#ce bout de code permet de récupérer l'une des recettes sur laquelle on a cliqué


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

    conn.close()
    return render_template('Unerecette.html', recipe=recipe, equipements=equipements, steps=steps)


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
    conn.close()
    if not user:
        return redirect(url_for('login'))
    return render_template('profil.html', username=user['Username'], firstname=user['FirstName'], lastname=user['LastName'])

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
                session["user"] = username
                return redirect("/")
        
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

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
    if "user" not in session:
        return redirect(url_for('login'))
    note = int(request.form.get('note', 0))
    user = session["user"]
    conn = sqlite3.connect('BDD.db')
    # À adapter selon ta table de notes (exemple: Recette_Note avec Recette_id, user, note)
    conn.execute("INSERT INTO Recette_Note (Recette_id, user, note) VALUES (?, ?, ?)", (recette_id, user, note))
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


if __name__ == '__main__':
    app.run(debug=True)



