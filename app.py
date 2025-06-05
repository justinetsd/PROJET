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
    recipes = conn.execute('SELECT * FROM recettes').fetchall()
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
@app.route('/recette/<int:recipe_id>') #route d'une recette
def recette(recipe_id):
    conn = sqlite3.connect('BDD.db')
    conn.row_factory = sqlite3.Row
    recipe = conn.execute('SELECT * FROM recettes WHERE id = ?', (recipe_id,)).fetchone()
    conn.close()
    
    if recipe is None:
        return "recettes not found", 404
    
    return render_template('Unerecette.html', recipe=recipe)



def hashage(password, rand, salt):
    combined = f"{password}{rand}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()

@app.route('/signin', methods=['GET', 'POST']) #route d'inscription
def signin(db_name="BDD.db"):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Check if the username already exists
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cur.fetchone():
            conn.close()
            return render_template("signin.html", error="Username already exists")

        # Generate random values for salt and rand
        rand = os.urandom(16).hex()
        salt = os.urandom(16).hex()

        # Hash the password with the random values
        hashed_password = hashage(password, rand, salt)

        # Insert the new user into the database
        cur.execute("INSERT INTO users (username, rand, salt, hash) VALUES (?, ?, ?, ?)",
                    (username, rand, salt, hashed_password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signin.html")

@app.route('/login', methods=['GET', 'POST']) #route de connexion
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute("SELECT rand, salt, hash FROM users WHERE username = ?", (username,))
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
    return render_template('été.html')

@app.route('/automne')
def automne():
    return render_template('automne.html')

@app.route('/hiver')
def hiver():
    return render_template('hiver.html')

@app.route('/printemps')
def printemps():
    return render_template('printemps.html')
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

if __name__ == '__main__':
    app.run(debug=True)
