import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/enternew')
def enternew():
    return render_template('food.html')


@app.route('/addfood', methods=['POST'])
def addfood():
    name = request.form['name']
    calories = request.form['calories']
    cuisine = request.form['cuisine']
    is_vegetarian = request.form['is_vegetarian']
    is_gluten_free = request.form['is_gluten_free']

    insert_new_food(name, calories, cuisine, is_vegetarian, is_gluten_free)

    return render_template('result.html', message=f'''Name: {name}
                                                     Calories: {calories}
                                                     Cuisine: {cuisine}
                                                     Vegetarian? {is_vegetarian}
                                                     Gluten Free? {is_gluten_free}''')


@app.route('/favorite')
def favorite():
    favorite_food = 'Pizza'
    result = find_by_name(favorite_food)
    return jsonify(result)


@app.route('/search')
def search():
    search_term = request.args.get('name', '')
    result = search_by_name(search_term)
    return jsonify(result)


@app.route('/drop')
def drop():
    drop_table('foods')
    return 'dropped'


def insert_new_food(name, calories, cuisine, is_vegetarian = 'No',
                    is_gluten_free = 'No'):
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute('INSERT INTO FOODS VALUES (?, ?, ?, ?, ?)', (name, calories, cuisine, is_vegetarian, is_gluten_free))
    connection.commit()
    connection.close()


def find_by_name(food_name):
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute('SELECT * FROM foods WHERE name = ?', (food_name,))
    result = c.fetchone()
    connection.close()
    return result


def search_by_name(name):
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute('SELECT * FROM foods WHERE name = ?', (name,))
    result = c.fetchall()
    connection.close()
    return result


def drop_table(table_name):
    connection = sqlite3.connect('database.db')
    connection.execute(f'DROP TABLE {table_name}')
    connection.close()
