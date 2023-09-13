import os
import sys

if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    import fcntl
else:
    # Handle the case where fcntl is not available on Windows
    pass
from flask import Flask, request, jsonify, abort
from flaskext.mysql import MySQL
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
mysql = MySQL(app)
# con = mysql.connect()
# cursor = con.cursor()

def is_valid_name(name):
    # validation logic for string input
    return isinstance(name, str) or not name.isalpha() and len(name) > 0

@app.route('/api/', methods=['GET'])
# for testing purpose
def get_names():
    """Get all names."""
    cur = mysql.connect().cursor()
    cur.execute('SELECT * FROM persons')
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


@app.route('/api', methods=['POST'])
def create_name():
    """Create a new name."""
    try:
        # Get the name from the request body
        data = request.get_json()
        name = data.get('name')
        #name = request.form.get('name')

        # Validate the name
        if not isinstance(name, str) or  not name.isalpha(): # and len(name) > 2:
            return jsonify({'error': 'Name must be a string'}), 400
        else:
            # Insert the name into the database
            connection= mysql.connect()
            cursor = connection.cursor()
            cursor.execute('INSERT INTO persons (name) VALUES (%s)', [name])
            #cursor.close()
            
            # Commit changes to the database
            connection.commit()

            return jsonify({'message': 'Name added to the database successfully', "name":name}), 201
    except Exception as e:
        # Rollback changes if an error occurs
        connection.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/<name>', methods=['PUT'])
def update_name(name):
    """Update a name."""
    if not isinstance(name, str)or not name.isalpha():
        return jsonify({'error': 'Name must be a string'})
    else:
        data = request.get_json()
        new_name = data.get('new_name')
        #new_name = request.json.get('new_name')
        connection= mysql.connect()
        cursor = connection.cursor()
        cursor.execute('UPDATE persons SET name=%s WHERE name=%s',[new_name, name])
        #cursor.close()
        
        # Commit changes to the database
        connection.commit()

        # Check if the name was updated successfully
        if cur.rowcount == 1:
            return jsonify({'message': 'Name updated successfully', "name":new_name})
        else:
            return jsonify({'error': 'Name not found'})

@app.route('/api/<name>', methods=['DELETE'])
def delete_name(name):
    try:
        """Delete a name."""
        # Validate the name
        if not is_valid_name(name):
            return jsonify({"error": "Invalid name"}), 400
        else:
            connection= mysql.connect()
            cursor = connection.cursor()
            cursor.execute('DELETE FROM persons WHERE name = %s', [name])
            #cur.close()
            
            # Commit changes to the database
            connection.commit()

            return jsonify({'message': 'Name deleted', "name":name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
