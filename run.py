import os
import sys

if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    import fcntl
else:
    # Handle the case where fcntl is not available on Windows
    pass
from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
mysql = MySQL(app)

@app.route('/api', methods=['GET'])
def get_names():
    """Get all names."""
    cur = mysql.connect().cursor()
    cur.execute('SELECT name FROM persons')
    names = cur.fetchall()
    cur.close()

    return jsonify(names)


@app.route('/api/<name>', methods=['GET'])
def get_name(name):
    """Get a name by name."""
    if not isinstance(name, str) or not name.isalpha():
        return jsonify({'error': 'Invalid name format'})
    else:
        cur = mysql.connect().cursor()
        cur.execute('SELECT name FROM persons WHERE name = %s', [name])
        result = cur.fetchone()
        cur.close()

        if result is None:
            return jsonify({'error': 'Name not found'})

        return jsonify({'name': result[0]})


@app.route('/api/<name>', methods=['POST'])
def create_name(name):
    """Create a new name."""
    if not isinstance(name, str) or  not name.isalpha():
        return jsonify({'error': 'Name must be a string'})
    else:
        cur = mysql.connect().cursor()
        cur.execute('INSERT INTO persons (name) VALUES (%s)', [name])
        cur.close()

        return jsonify({'message': 'Name created'})


@app.route('/api/<name>', methods=['PUT'])
def update_name(name):
    """Update a name."""
    if not isinstance(name, str)or not name.isalpha():
        return jsonify({'error': 'Name must be a string'})
    else:
        new_name = request.json.get('name')
        cur = mysql.connect().cursor()
        cur.execute('UPDATE persons SET name = %s WHERE name = %s', [new_name, name])
        cur.close()

        return jsonify({'message': 'Name updated'})


@app.route('/api/<name>', methods=['DELETE'])
def delete_name(name):
    """Delete a name."""
    if not isinstance(name, str)or not name.isalpha():
        return jsonify({'error': 'Name must be a string'})
    else:
        cur = mysql.connect().cursor()
        cur.execute('DELETE FROM persons WHERE name = %s', [name])
        cur.close()

        return jsonify({'message': 'Name deleted'})


if __name__ == '__main__':
    app.run(debug=True)
