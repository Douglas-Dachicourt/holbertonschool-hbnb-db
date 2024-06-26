from sqlalchemy import inspect
from app import app
from db import db
from models.users import User

def run_tests():
    with app.app_context():
        # Créer les tables
        print("Creating database tables...")
        db.create_all()
        print("Tables created.")

        # Vérifier les tables
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tables in the database: {tables}")

        # Ajouter un utilisateur
        new_user = User(email='test@example.com', first_name='Test', last_name='User', password='password')
        db.session.add(new_user)
        db.session.commit()
        print("Added new user.")

        # Vérifier l'ajout de l'utilisateur
        users = User.query.all()
        for user in users:
            print(f"User: {user.email}, {user.first_name}, {user.last_name}")

if __name__ == "__main__":
    run_tests()