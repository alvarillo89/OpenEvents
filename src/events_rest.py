# -*- coding: utf-8 -*-

import hug
from falcon import HTTP_404, HTTP_200, HTTP_201, HTTP_409
from Events import Events


# Create Events object:
# By doing this we ensure that the layered architecture is respected:
event = Events()


@hug.get("/event/title/{title}")
def getEvent(title, response):
    res = event.search_by_title(title)
    if res == []:
        response.status = HTTP_404
        return "Event not found"
    else:
        response.status = HTTP_200
        return res[0]


@hug.post("/event")
def addEvent(body, response):
    try:
        id = event.create(body['title'], body['organizer'], body['date'], body['address'],
            body['description'], body['prize'], body['tickets_availables'])
        response.status = HTTP_201
        return "Event Added. ID={}".format(id)
    except ValueError:
        response.status = HTTP_409
        return "An Event with title {} already exists".format(body['title'])


@hug.delete("/event/id/{id}")
def removeEvent(id, response):
    try:
        event.remove(id)
        response.status = HTTP_200
        return "Event removed"
    except LookupError:
        response.status = HTTP_404
        return "There is no event with that ID"


@hug.put("/event/id/{id}")
def updateEvent(id, body, response):
    try:
        event.modify(id, body)
        response.status = HTTP_200
        return "Event updated"
    except KeyError:
        response.status = HTTP_409
        return "Unknown field in new values"
    except LookupError:
        response.status = HTTP_404
        return "There is no event with that ID"