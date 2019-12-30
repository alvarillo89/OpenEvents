# -*- coding: utf-8 -*-

import os
import sys
import hug
import unittest
import datetime
from celery.result import AsyncResult
from unittest.mock import MagicMock
from unittest.mock import patch
from falcon import HTTP_200, HTTP_404

import sys
sys.path.append("src")

import tickets_tasks
import tickets_rest


class TestTicketsRestTasks(unittest.TestCase):

    def setUp(self):
        # We use a mock for simulate the datamanager:
        tickets_tasks.tickets.data_manager = MagicMock()
        self.mock = tickets_tasks.tickets.data_manager

        # Create a sample event:
        self.sample_event = dict(
            _id='000000000000000000000000',
            title="Sample title",
            organizer="An organizer",
            date=datetime.datetime(2020, 5, 17, 18, 30),
            address="In some place",
            description="Just a example event",
            prize=3.0,
            tickets_availables=10
        )

        # Create a sample buyer:
        self.sample_buyer = dict(
            name="Sample buyer name",
            email="buyer@email.com"
        )

        # Create a sample register:
        self.sample_register = { 
            "_id" : "5e0a21eb8b7a247c21efe3d9", 
            "owner_name" : "Sample buyer name", 
            "owner_email" : "buyer@email.com", 
            "buy_date" : "2019-12-30T17:12:27.724Z", 
            "ticket_id" : "d9c382772d594a47960ab74c4b28397e-000000000000000000000000-Samplebuyername"
        }


    def test_celery_task(self):
        """ Test if celery task is performing correctly """
        out = tickets_tasks.get_ticket.run(self.sample_buyer, self.sample_event)
        self.assertTrue(os.path.isfile(out))
        if sys.version_info[1] > 5:
            self.mock.insert.assert_called()


    @patch('tickets_tasks.get_ticket.delay')
    def test_task_post(self, mock_get_ticket):
        """ The the post request for purchase a ticket """
        # Configure the return value:
        mock_get_ticket.return_value = AsyncResult("sample_task_id")
        # Configure the payload:
        payload = dict(event=self.sample_event, buyer=self.sample_buyer)
        request = hug.test.post(tickets_rest, "/ticket", payload)
        self.assertEqual(request.status, HTTP_200)
        self.assertEqual(request.data, "sample_task_id")
        self.sample_event['date'] = "2020-05-17T18:30:00"
        mock_get_ticket.assert_called_with(self.sample_buyer, self.sample_event)


    @patch('tickets_rest.AsyncResult')
    def test_task_get(self, mock_async):
        """ Test the get request of a previous posted task """
        # Configure the mock return value:
        other_mock = MagicMock()
        other_mock.result = "/tmp/tmp_dir/Ticket_12345678.pdf"
        mock_async.return_value = other_mock
        request = hug.test.get(tickets_rest, "/ticket/sample_task_id")
        mock_async.assert_called_with("sample_task_id")
        self.assertEqual(request.status, HTTP_404)
        self.assertEqual(request.data, "File not found!")

    
    def test_is_valid(self):
        """ Test the validation of a ticket """
        # Check valid id:
        self.mock.get.return_value = self.sample_register
        request = hug.test.get(tickets_rest, "/ticket/isvalid/" + self.sample_register['ticket_id'])
        self.assertEqual(request.status, HTTP_200)
        self.assertEqual(request.data, "The ticket is valid")
        self.mock.get.assert_called_with(key="ticket_id", value=self.sample_register['ticket_id'])
        # Check invalid id:
        self.mock.reset_mock()
        self.mock.get.return_value = None
        request = hug.test.get(tickets_rest, "/ticket/isvalid/wrong_ticket_id")
        self.assertEqual(request.status, HTTP_200)
        self.assertEqual(request.data, "The ticket is invalid")
        self.mock.get.assert_called_with(key="ticket_id", value="wrong_ticket_id")


if __name__ == "__main__":
    unittest.main(verbosity=2)   