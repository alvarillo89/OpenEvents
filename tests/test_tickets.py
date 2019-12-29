# -*- coding: utf-8 -*-

import os
import uuid
import datetime
import unittest
from unittest.mock import MagicMock
from reportlab.lib.utils import ImageReader

import sys
sys.path.append("src")

import Tickets

class TestTickets(unittest.TestCase):

    def setUp(self):
        # We use a mock for simulate the datamanager:
        self.mock = MagicMock()
        # Create a Ticket class object with the mock:
        self.ticket = Tickets.Tickets(data_manager=self.mock)
        # Create a sample buyer:
        self.sample_buyer = dict(
            name="Sample buyer name",
            email="buyer@email.com"
        )
        # Create a sample event:
        self.sample_event = dict(
            _id="000000000000000000000000",
            title="Sample title",
            organizer="An organizer",
            date=datetime.datetime(2020, 5, 17, 18, 30),
            address="In some place",
            description="Just a example event",
            prize=3.0,
            tickets_availables=10
        )
        # Create a sample ticket id:
        self.sample_ticket_id = uuid.uuid4().hex + '-' + self.sample_event['_id'] + '-' \
            + self.sample_buyer['name'].replace(" ", "")


    def test_generate_barcode(self):
        """ Test the generation of a barcode and ticket id """
        barcode, ticket_id = self.ticket.generate_barcode(self.sample_event['_id'], 
            self.sample_buyer['name'])

        self.assertTrue(self.sample_event['_id'] in ticket_id)
        self.assertTrue(self.sample_buyer['name'].replace(" ", "") in ticket_id)
        self.assertEqual(len(ticket_id), 58+len(self.sample_buyer['name'].replace(" ", "")))
        self.assertIsInstance(barcode, ImageReader)


    def test_generate_ticket(self):
        """ Test the generation of a ticket """
        barcode, _ = self.ticket.generate_barcode(self.sample_event['_id'], 
            self.sample_buyer['name'])
        file = self.ticket.generate_ticket(self.sample_buyer, self.sample_event, barcode)

        self.assertTrue("tmp" in file)
        self.assertTrue("Ticket" in file)
        self.assertTrue(".pdf" in file)
        self.assertTrue(os.path.isfile(file))


    def test_is_valid(self):
        """ Test the check if certain ticket id is valid or not """
        # Config mock return value:
        register = dict(
            owner_name=self.sample_buyer['name'],
            owner_email=self.sample_buyer['email'],
            buy_date=datetime.datetime.today(),
            ticket_id=self.sample_ticket_id
        )
        self.mock.get.return_value = register
        res = self.ticket.is_valid(self.sample_ticket_id)
        
        self.assertTrue(res)
        self.mock.get.assert_called_with(key='ticket_id', value=self.sample_ticket_id)

        # Non existing ticket_id:
        self.mock.reset_mock()
        self.mock.get.return_value = None
        res = self.ticket.is_valid(self.sample_ticket_id)

        self.assertFalse(res)
        self.mock.get.assert_called_with(key='ticket_id', value=self.sample_ticket_id)


    def test_buy_ticket(self):
        """ Test  the purchase of a ticket """
        file = self.ticket.buy_ticket(self.sample_buyer, self.sample_event)
        # Get the inserted register:
        inserted_res = self.mock.insert.call_args[0][0]

        self.assertTrue("tmp" in file)
        self.assertTrue("Ticket" in file)
        self.assertTrue(".pdf" in file)
        self.assertTrue(os.path.isfile(file))
        self.assertEqual(inserted_res['owner_name'], self.sample_buyer['name'])
        self.assertEqual(inserted_res['owner_email'], self.sample_buyer['email'])
        self.assertIsInstance(inserted_res['buy_date'], datetime.datetime)
        self.assertEqual(len(inserted_res['ticket_id']), 
            58+len(self.sample_buyer['name'].replace(" ", "")))
        

if __name__ == "__main__":
    unittest.main(verbosity=2)  