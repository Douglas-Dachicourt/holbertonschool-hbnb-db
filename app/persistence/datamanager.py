import json
import datetime
from persistence.ipersistencemanager import IPersistenceManager


class DataManager(IPersistenceManager):
    """
    Defines the subclass DataManager that inherits from
    IPersistenceManager
    """

    def __init__(self, flag):
        """Method used to initialize DataManager"""
        self.set_file_path(flag)

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
        Methdod used to save data(entity) into a JSON file
        """
        data = []
        try:
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            pass
        data.append(entity)

        with open(self.file_path, 'w', encoding='UTF-8') as f:
            json.dump(data, f, indent=4)

    def get(self, entity, id):
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

    def delete(self, entity, id):
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

    def update(self, entity, id):
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
