# -*- coding: utf-8 -*-

import uuid

class Events:
    def __init__(self):
        self.event_list = []


    def create(self, title, organizer, date, address, description, prize, tickets_availables):
        if self.search_by_title(title) == []:
            ID = uuid.uuid1().hex
            item = dict(
                ID=ID,
                title=title,
                organizer=organizer,
                date=date,
                address=address,
                description=description,
                prize=prize,
                tickets_availables=tickets_availables
            )
            self.event_list.append(item)
            return ID
        else:
            raise ValueError("An event with that title already exists")
    

    def search_by_title(self, title):
        return [event for event in self.event_list if event["title"]==title]
    

    def search_by_id(self, id):
        res = [event for event in self.event_list if event["ID"]==id]

        if res == []:
            raise LookupError("There is no event with that ID")

        return res


    def remove(self, id):
        event = self.search_by_id(id)
        self.event_list.remove(event[0])
    

    def modify(self, id, new_values):
        event = self.search_by_id(id)
        index = self.event_list.index(event[0])

        for key in new_values.keys():
            if key not in event[0].keys():
                raise KeyError("An event does not have a field called " + str(key))
            if key == "ID":
                raise KeyError("ID field cannot been modified")
            self.event_list[index][key] = new_values[key]