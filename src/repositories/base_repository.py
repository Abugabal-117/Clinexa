from abc import ABC, abstractmethod
from core.csv_manager import CSVManager


class BaseRepository(ABC):
    def __init__(self, filename, id_field='user_id'):
        self.csv_manager = CSVManager()
        self.filename = filename
        self.id_field = id_field
    
    @abstractmethod
    def get_fieldnames(self):
        pass
    
    @abstractmethod
    def to_model(self, data):
        pass
    
    def get_all(self):
        data = self.csv_manager.read_csv(self.filename)
        results = []
        for row in data:
            results.append(self.to_model(row))
        return results
    
    def get_by_id(self, entity_id):
        data = self.csv_manager.read_csv(self.filename)
        for row in data:
            if row.get(self.id_field) == str(entity_id):
                return self.to_model(row)
        return None
    
    def save(self, entity):
        data = self.csv_manager.read_csv(self.filename)
        entity_dict = entity.to_dict()
        
        updated = False
        for i, row in enumerate(data):
            if row.get(self.id_field) == entity_dict[self.id_field]:
                data[i] = entity_dict
                updated = True
                break
        
        if not updated:
            data.append(entity_dict)
        
        self.csv_manager.write_csv(self.filename, data, self.get_fieldnames())
        return entity
    
    def delete(self, entity_id):
        data = self.csv_manager.read_csv(self.filename)
        new_data = []
        for row in data:
            if row.get(self.id_field) != str(entity_id):
                new_data.append(row)
                
        self.csv_manager.write_csv(self.filename, new_data, self.get_fieldnames())
    
    def find_by_field(self, field_name, value):
        data = self.csv_manager.read_csv(self.filename)
        results = []
        for row in data:
            if row.get(field_name) == str(value):
                results.append(self.to_model(row))
        return results
