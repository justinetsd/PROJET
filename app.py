from flask import Flask, render_template
from flask import request, session, redirect, render_template
import hashlib
import os
import sqlite3

app = Flask(__name__)

def get_recipes(): #recette
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return recipes

@app.route('/') #route par défaut
def index():
    recipes = get_recipes()
    return render_template('index.html', recipes=recipes)


def hashage(password, rand, salt):
    combined = f"{password}{rand}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()

@app.route('/signin', methods=['GET', 'POST']) #route d'inscription
def signin(db_name="users.db"):
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




if __name__ == '__main__':
    app.run(debug=True)
