# Authentication System API

This is my backend project for the authentication system assignment.

The project is a simple REST API built with FastAPI and MongoDB. It allows users to register and login, and it uses JWT tokens to protect some routes. There are two user types in the system: `admin` and `client`.

There is no frontend in this project. The API can be tested using Swagger or Postman.

## Project Features

- Register a new user
- Login with email and password
- Hash passwords before saving them
- Generate JWT access tokens
- Allow only admins to manage users
- Return simple user statistics
- Store users in MongoDB

## Technologies Used

- Python
- FastAPI
- MongoDB
- PyMongo
- Pydantic
- JWT
- passlib with bcrypt

## Project Structure

```text
auth_system_api/
|
+-- app/
|   +-- main.py
|   +-- config.py
|   +-- database.py
|   +-- models.py
|   +-- schemas.py
|   +-- auth.py
|   +-- dependencies.py
|   +-- crud.py
|   +-- routes/
|       +-- auth_routes.py
|       +-- user_routes.py
|       +-- stats_routes.py
|
+-- .env.example
+-- requirements.txt
+-- README.md
```

## How to Run the Project

First, open the terminal inside the project folder:

```bash
cd auth_system_api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

On Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the main project folder. You can copy the example file:

```bash
copy .env.example .env
```

Then put the MongoDB connection string and the other settings inside the `.env` file.

Example:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=auth_system_db
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

After that, run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The project will run on:

```text
http://127.0.0.1:8000
```

Swagger will open from:

```text
http://127.0.0.1:8000/docs
```

## How to Test

The API can be tested from Swagger:

1. Open `http://127.0.0.1:8000/docs`
2. Use `/register` to create a user.
3. Use `/login` to get the access token.
4. Click `Authorize` and paste the token.
5. Test the protected admin routes.

## Main Endpoints

```text
POST   /register
POST   /login
GET    /users
PUT    /users/{user_id}
DELETE /users/{user_id}
GET    /stats/count
GET    /stats/average-age
GET    /stats/top-cities
```

## Notes

- The password is saved as a hashed password, not plain text.
- The admin routes can only be used by users with type `admin`.
- The `.env` file is not included because it contains private settings.
- The MongoDB database is connected using the connection string from `.env`.
