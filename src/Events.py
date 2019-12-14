# -*- coding: utf-8 -*-

class Events:
    # Dependency injection:
    def __init__(self, data_manager):
        self.data_manager = data_manager


    def create(self, title, organizer, date, address, description, prize, tickets_availables):
        if self.search_by_title(title) == None:
            item = dict(
                title=title,
                organizer=organizer,
                date=date,
                address=address,
                description=description,
                prize=prize,
                tickets_availables=tickets_availables
            )
            _id = self.data_manager.insert(item)
            return _id
        else:
            raise ValueError("An event with that title already exists")
    

    def search_by_title(self, title):
        return self.data_manager.get_title(title)
    

    def search_by_id(self, id):
        res = self.data_manager.get_id(id)

        if res == None:
            raise LookupError("There is no event with that ID")

        return res


    def remove(self, id):
        # First test if an event with that id exists:
        self.search_by_id(id)
        self.data_manager.delete(id)
    

    def modify(self, id, new_values):
        event = self.search_by_id(id)

        # Check keys correction:
        for key in new_values.keys():
            if key not in event.keys():
                raise KeyError("An event does not have a field called " + str(key))
            if key == "_id":
                raise KeyError("ID field cannot been modified")
        
        self.data_manager.update(id, new_values)