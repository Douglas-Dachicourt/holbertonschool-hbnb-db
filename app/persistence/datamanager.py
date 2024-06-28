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
        """
        Initializes DataManager instance.

        Args:
        flag (str): Flag parameter used to set file path.

        Sets up DataManager instance with appropriate file path and
        determines persistence mode based on environment variable
        or defaults to 'file'.

        Attributes:
        persistence_mode (str): Mode of persistence for data storage,
            either 'file' or 'database'.
    """
        self.set_file_path(flag)
        self.persistence_mode = os.getenv("PERSISTENCE_MODE", "file")

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
        """
        Saves the entity based on the current persistence mode.

        Args:
            entity (dict or SQLAlchemy model): Entity to be saved.
                If using 'file' mode, expects a dictionary.
                If using 'database' mode, expects a SQLAlchemy model.

        Raises:
            ValueError: If persistence mode is not supported.
        """
        if self.persistence_mode == "file":
            self.save_to_file(entity)
        elif self.persistence_mode == "database":
            self.save_to_database(entity)
        else:
            raise ValueError(f"Unsupported persistence" +
                             "mode: {self.persistence_mode}")

    def get(self, entity, id):
        """
        Retrieves the entity with the specified id based on the current
        persistence mode.

        Args:
            entity (type): Type of entity to retrieve (used in database mode).
            id (str): Unique identifier of the entity.

        Returns:
            dict or SQLAlchemy model: Retrieved entity.

        Raises:
            ValueError: If persistence mode is not supported.
        """
        if self.persistence_mode == "file":
            return self.get_from_file(entity, id)
        elif self.persistence_mode == "database":
            return self.get_from_database(entity, id)
        else:
            raise ValueError(f"Unsupported persistence" +
                             "mode: {self.persistence_mode}")

    def delete(self, entity, id):
        """
        Deletes the entity with the specified id based on the current
        persistence mode.

        Args:
            entity (type): Type of entity to delete (used in database mode).
            id (str): Unique identifier of the entity.

        Raises:
            ValueError: If persistence mode is not supported.
        """
        if self.persistence_mode == "file":
            self.delete_from_file(entity, id)
        elif self.persistence_mode == "database":
            self.delete_from_database(entity, id)
        else:
            raise ValueError(f"Unsupported persistence" +
                             "mode: {self.persistence_mode}")

    def update(self, entity, id):
        """
        Updates the entity with the specified id based on the current
        persistence mode.

        Args:
            entity (dict or SQLAlchemy model): Updated entity.
                If using 'file' mode, expects a dictionary.
                If using 'database' mode, expects a SQLAlchemy model.
            id (str): Unique identifier of the entity.

        Raises:
            ValueError: If persistence mode is not supported.
        """
        if self.persistence_mode == "file":
            self.update_file(entity, id)
        elif self.persistence_mode == "database":
            self.update_database(entity, id)
        else:
            raise ValueError(f"Unsupported persistence" +
                             "mode: {self.persistence_mode}")

    def save_to_file(self, entity):
        """
        Saves the entity to a JSON file.

        Args:
            entity (dict): Entity data to be saved into the file.

        Raises:
            FileNotFoundError: If the file specified by self.file_path does
            not exist.
            Exception: For any other unexpected error during file operation.
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
            raise e
        except Exception as e:
            raise e

    def get_from_file(self, entity, id):
        """
        Retrieves the entity from a JSON file based on its id.

        Args:
            entity (type): Type of entity to retrieve (not directly used in
            file
            mode).
            id (str): Unique identifier of the entity.

        Returns:
            dict: Retrieved entity data.

        Raises:
            FileNotFoundError: If the file specified by self.file_path does not
            exist.
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
        Deletes the entity from a JSON file based on its id.

        Args:
            entity (type): Type of entity to delete (not directly used in file
            mode).
            id (str): Unique identifier of the entity.

        Raises:
            FileNotFoundError: If the file specified by self.file_path does not
            exist.
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
        Updates the entity in a JSON file based on its id.

        Args:
            entity (dict): Updated entity data to replace existing data.
            id (str): Unique identifier of the entity.

        Raises:
            FileNotFoundError: If the file specified by self.file_path does not
            exist.
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
        """
        Saves the entity to the database.

        Args:
            entity (SQLAlchemy model): Entity object to be saved.
        """
        db.session.add(entity)
        db.session.commit()

    def get_from_database(self, entity, id):
        """
        Retrieves the entity from the database based on its id.

        Args:
            entity (type): Type of entity to retrieve (used in database mode).
            id (str): Unique identifier of the entity.

        Returns:
            SQLAlchemy model: Retrieved entity object.
        """
        return db.session.query(entity).filter_by(id=id).first()

    def delete_from_database(self, entity, id):
        """
        Deletes the entity from the database based on its id.

        Args:
            entity (type): Type of entity to delete (used in database mode).
            id (str): Unique identifier of the entity.
        """

        entity_to_delete = db.session.query(entity).filter_by(id=id).first()
        if entity_to_delete:
            db.session.delete(entity_to_delete)
            db.session.commit()

    def update_database(self, entity, id, data):
        """
        Updates the entity in the database based on its id.

        Args:
            entity (SQLAlchemy model): Updated entity object to replace
            existing data.
            id (str): Unique identifier of the entity.
        """
        entity_to_update = db.session.query(entity).filter_by(id=id).first()
        if entity_to_update:
            for key, value in data.items():
                setattr(entity_to_update, key, value)
            db.session.commit()
