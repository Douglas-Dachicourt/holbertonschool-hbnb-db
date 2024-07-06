# HBNB Project part 2

## Description

The HBNB project is part of the Holberton School curriculum. It aims to create a basic replica of an Airbnb-like application, allowing CRUD operations (Create, Read, Update, Delete) on two different databases : sqlite for development mode, postgresql for production mode.

## Features

- Create, update, and delete users.
- Add, modify, or delete rental places.
- Create, modify, or delete amenities for a place.
- Post, update, or delete reviews for places.
- Save API and interact with on sqlite/postgres databases.

## Technologies Used

- **Python 3.10.12**: Main programming language.
- **Flask**: Framework to handle the RESTful API.
- **Gunicorn**: WSGI server to deploy the application.
- **Unittest**: Unit testing module.
- **SwaggerUI**: API documentation.
- **Docker**: Containerization of the application.
- **GitHub Actions**: Continuous integration and deployment.

### Future Implementations

- **CI/CD**: improve our GitHUB Actions workflow to achieve Continuous Implementation and Continuous Development.
- **SQLAlchemy**: or another database toolkit, to migrate our JSON base system.
- **Security**: will be enforced and based on authentification tokens amongst other systems.
- **Front end**: a proper website, with neat HTML, CSS and JavaScript.

## Installation

### Prerequisites

- Docker installed on your machine.

### Installation Steps

1. **Clone the repository**

    ```sh
    git clone https://github.com/Douglas-Dachicourt/holbertonschool-hbnb-db
    cd holbertonschool-hbnb-db
    ```

2. **Test sqlite or postgresSQL databases**

    - SQLITE/POSTGRESSQL => development database/production <br>
    <t> You have to edit the .env file first to make sure the mode you want is active (uncomment the mode you need): <br>
    <br>
    *EXEMPLE*

     ```sh
    # development mode, sqlite
    ENV=development
    DATABASE_TYPE=sqlite
    DATABASE_URL=sqlite:///development.db

    # production mode, postgres
    #ENV=production
    #DATABASE_TYPE=postgresql
    #DATABASE_URL=postgresql://maxdoug:projet2@localhost/production

    JWT_SECRET_KEY= 2c1br3mt2wkkcagl68aqh5iml
    ```
 => THEN RUN THE server with the following line command `python app/app.py` <br>

3. **Build the Docker image**

    ```sh
    docker image build . -t "hbnb"
    ```

4. **Run the Docker container**

    By default, the application runs on port 8000.

    ```sh
    docker run -d -p 8000:8000 -v hbnb_data:/home/hbnb/hbnb_data hbnb
    ```

    ```

    To launch the unittest
    ``` sh
     python3 -m unittest tests/test_auth.py
     python3 -m unittest tests/test_db_sqlite_operations.py
     ...
    ```


## Usage

Once the container is running, you can access the API at `http://localhost`.

API documentation is available here:

`http://localhost/api/docs` 


## Contributors

- [Douglas **DACHICOURT**](https://github.com/Douglas-Dachicourt)
- [Maxime **MARTIN**](https://github.com/cosmos510)
- [Sofiane **ARFANE**](https://github.com/Sofiane74100)
