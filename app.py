from flask import Flask, render_template
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

if __name__ == '__main__':
    app.run(debug=True)
