# Person Flask MySQL API

This is a simple RESTful API built with Flask and MySQL for managing names. It allows you to perform basic CRUD (Create, Read, Update, Delete) operations on a list of names stored in a MySQL database.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed.

- MySQL server installed and running. (www.freesqldatabase.com)

- Required Python packages are installed. You can install them using pip with the provided requirements.txt file.

## Getting Started

1. Clone this repository to your local machine:
   `git clone <repository_url>`

2. Navigate to the project directory:
   `cd flask-mysql-api`

3. Create a .env file in the project root and define your MySQL database configuration as follows:

```
MYSQL_DATABASE_USER=your_mysql_user`
MYSQL_DATABASE_PASSWORD=your_mysql_password
MYSQL_DATABASE_DB=your_database_name
MYSQL_DATABASE_HOST=your_database_host
```

4. Install the required Python packages:
   `pip install -r requirements.txt`

5. Run the Flask application:
   `python run.py`
   or
   `waitress-serve --host=0.0.0.0 --port=5000 run:app`
   or
   ` gunicorn -b 0.0.0.0:5000 run:app`

The API should now be running at http://localhost:5000.

## API Endpoints

- `GET /api`: Get a list of all names.

- `GET /api/<name>`: Get a name by name.

- `POST /api/<name>`: Create a new name.

- `PUT /api/<name>`: Update a name.

- `DELETE /api/<name>`: Delete a name.

## Usage

You can use any HTTP client or tools like curl to interact with the API. Here are some sample requests:

- Get all names:
  `curl http://localhost:5000/api`

- Get a name by name:
  `curl http://localhost:5000/api/John`

- Create a new name:
  `curl -X POST -H "Content-Type: application/json" -d '{"name": "Alice"}' http://localhost:5000/api/Alice`

- Update a name:
  `curl -X PUT -H "Content-Type: application/json" -d '{"name": "Bob"}' http://localhost:5000/api/Alice`

- Delete a name:
  `curl -X DELETE http://localhost:5000/api/Alice`

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](https://www.example.com) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](http://www.opensource.org/licenses/mit-license) file for details.
