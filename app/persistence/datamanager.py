import json
import datetime
from persistence.ipersistencemanager import IPersistenceManager
import os
from db import db

class DataManager(IPersistenceManager):
    """
    Defines the subclass DataManager that inherits from
    IPersistenceManager
    """

    def __init__(self, flag):
        """Method used to initialize DataManager"""
        self.set_file_path(flag)
        self.persistence_mode=os.getenv("PERSISTENCE_MODE", "file")

    def set_file_path(self, flag):
        """Sets in which json file data will be managed based on a flag"""
        if flag == 1:
            self.file_path = "/home/hbnb/hbnb_data/User.json"
        elif flag == 2:
            self.file_path = "/home/hbnb/hbnb_data/Place.json"
        elif flag == 3:
            self.file_path = "/home/hbnb/hbnb_data/Amenity.json"
        elif flag == 4:
            self.file_path = "/home/hbnb/hbnb_data/Review.json"
        elif flag == 5:
            self.file_path = "/home/hbnb/hbnb_data/cities.json"

        else:
            raise ValueError(f"Unsupported flag value: {flag}")

    def save(self, entity):
        if self.persistence_mode == "file":
            self.save_to_file(entity)
        elif self.persistence_mode == "database":
            self.save_to_database(entity)
        else:
            raise ValueError(f"Unsupported persistence mode: {self.persistence_mode}")

    def get(self, entity, id):
        if self.persistence_mode == "file":
            return self.get_from_file(entity, id)
        elif self.persistence_mode == "database":
            return self.get_from_database(entity, id)
        else:
            raise ValueError(f"Unsupported persistence mode: {self.persistence_mode}")

    def delete(self, entity, id):
        if self.persistence_mode == "file":
            self.delete_from_file(entity, id)
        elif self.persistence_mode == "database":
            self.delete_from_database(entity, id)
        else:
            raise ValueError(f"Unsupported persistence mode: {self.persistence_mode}")

    def update(self, entity, id):
        if self.persistence_mode == "file":
            self.update_file(entity, id)
        elif self.persistence_mode == "database":
            self.update_database(entity, id)
        else:
            raise ValueError(f"Unsupported persistence mode: {self.persistence_mode}")


    def save_to_file(self, entity):
        """
        Save data(entity) into a JSON file
        """
        try:
            if os.path.isfile(self.file_path):
                with open(self.file_path, 'r', encoding='UTF-8') as f:
                    data = json.load(f)
            else:
                data = []

            data.append(entity)

            with open(self.file_path, 'w', encoding='UTF-8') as f:
                json.dump(data, f, indent=4)

        except FileNotFoundError as e:
        # Gérer ou logger l'erreur selon votre besoin
            raise e
        except Exception as e:
        # Gérer ou logger d'autres exceptions
            raise e

    def get_from_file(self, entity, id):
        """
        Method used to get data(entity) from a JSON file
        """
        try:
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                data = json.load(f)
                for item in data:
                    if item["uniq_id"] == id:
                        return item
        except FileNotFoundError:
            pass

    def delete_from_file(self, entity, id):
        """
        Method used to delete data(entity) from a JSON file
        """

        try:
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                data = json.load(f)
                for item in data:
                    if item["uniq_id"] == id:
                        data.remove(item)
                        with open(self.file_path, 'w', encoding='UTF-8') as f:
                            json.dump(data, f, indent=4)
                        return
        except FileNotFoundError:
            pass

    def update_file(self, entity, id):
        """
        Method used to update data(entity) from a JSON file
        """
        try:
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                data = json.load(f)
            for item in data:
                if item["uniq_id"] == id:
                    data.remove(item)
                    entity["updated_at"] = datetime.datetime.now().isoformat()
                    data.append(entity)
                    with open(self.file_path, 'w', encoding='UTF-8') as f:
                        json.dump(data, f, indent=4)
                    return
        except FileNotFoundError:
            pass

    def save_to_database(self, entity):
        db.session.add(entity)
        db.session.commit()

    def get_from_database(self, entity, id):
        return db.session.query(entity).filter_by(uniq_id=id).first()

    def delete_from_database(self, entity, id):
        db.session.query(entity).filter_by(uniq_id=id).delete()
        db.session.commit()

    def update_database(self, entity, id):
        entity_to_update = db.session.query(entity).filter_by(uniq_id=id).first()
        entity_to_update.update(entity)
        db.session.commit()