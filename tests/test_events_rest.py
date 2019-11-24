# -*- coding: utf-8 -*-

import hug
import unittest
import datetime
from falcon import HTTP_404, HTTP_200, HTTP_201, HTTP_409

import sys
sys.path.append("src")

import events_rest


class TestEventsRest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Add a sample event to events object: """
        cls.sample_title = "An event"
        cls.sample_id = events_rest.event.create(
            title=cls.sample_title, organizer="An organizer",
            date=datetime.datetime(2020, 5, 17, 18, 30), address="In some place",
            description="Just a sample event", prize=8.0, tickets_availables=10
        )

    
    def test_get_ok(self):
        """ Test the get request of an existing event by title """
        request = hug.test.get(events_rest, "/event/title/" + self.sample_title)
        # Convert getted string date to datetime object:
        request.data["date"] = datetime.datetime.strptime(request.data["date"], '%Y-%m-%dT%H:%M:%S')
        self.assertEqual(request.status, HTTP_200)
        self.assertEqual(request.data, events_rest.event.search_by_title(self.sample_title)[0])


    def test_get_not_found(self):
        """ Test the get request of an non-existing event by title """
        request = hug.test.get(events_rest, "/event/title/thiseventdoesntexists")
        self.assertEqual(request.status, HTTP_404)
        self.assertEqual(request.data, "Event not found")

    
    def test_post_ok(self):
        """ Test the post request posting a new event """
        new_event = dict(
            title="Another event",
            organizer="Another organizer",
            date=datetime.datetime(2020, 6, 17, 17, 30),
            address="In another place",
            description="Just another example event",
            prize=5.0,
            tickets_availables=100
        )

        request = hug.test.post(events_rest, "/event", new_event)
        self.assertEqual(request.status, HTTP_201)
        self.assertTrue("Event Added. ID=" in request.data)
        # Get the ID:
        id = request.data[16:]
        # Check if an event with that title exists
        self.assertTrue(len(events_rest.event.search_by_id(id)) != 0)


    def test_post_conflict(self):
        """ Test the post request of an event with the same title of other """
        new_event = dict(
            title=self.sample_title,
            organizer="Doesn't matter",
            date=datetime.datetime(2020, 6, 17, 17, 30),
            address="Doesn't matter",
            description="Doesn't matter",
            prize=5.0,
            tickets_availables=100
        )

        request = hug.test.post(events_rest, "/event", new_event)
        self.assertEqual(request.status, HTTP_409)
        self.assertEqual(request.data, 
            "An Event with title {} already exists".format(self.sample_title))

    
    def test_delete_ok(self):
        """ Test the delete request of an existing event """
        # Add a event for remove it later:
        id = events_rest.event.create(title="Just for this test", organizer="Some guys",
            date=datetime.datetime(2020, 6, 17, 17, 30), address="Some place", description="...",
            prize=10.0, tickets_availables=100
        )

        response = hug.test.delete(events_rest, "/event/id/" + id)
        self.assertEqual(response.status, HTTP_200)
        self.assertEqual(response.data, "Event removed")

        # Ensure that the event had been removed:
        with self.assertRaises(LookupError):
            events_rest.event.search_by_id(id)


    def test_delete_not_found(self):
        """ Test the delete request of a non-existing event """
        response = hug.test.delete(events_rest, "/event/id/thiseventdoesntexists")
        self.assertEqual(response.status, HTTP_404)
        self.assertEqual(response.data, "There is no event with that ID")


    def test_put_ok(self):
        """ Test the modification of a existing event """
        new_data = dict(description="A new description", prize=800.0)
        response = hug.test.put(events_rest, "event/id/" + self.sample_id, new_data)
        self.assertEqual(response.status, HTTP_200)
        self.assertEqual(response.data, "Event updated")
        # Ensure that event had been modified:
        event = events_rest.event.search_by_title(self.sample_title)[0]
        self.assertEqual(event['description'], new_data['description'])
        self.assertEqual(event['prize'], new_data['prize'])


    def test_put_fails(self):
        """ Test the modification of a non-existing event and the modification of a bad key """
        new_data = dict(badKey="This is bad")
        # Non existing event:
        response = hug.test.put(events_rest, "event/id/nonexistingid", new_data)
        self.assertEqual(response.status, HTTP_404)
        self.assertEqual(response.data, "There is no event with that ID")
        # Bad key:
        response = hug.test.put(events_rest, "event/id/" + self.sample_id, new_data)
        self.assertEqual(response.status, HTTP_409)
        self.assertEqual(response.data, "Unknown field in new values")


if __name__ == "__main__":
    unittest.main(verbosity=2)    