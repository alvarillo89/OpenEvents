# -*- coding: utf-8 -*-

import os
from celery import Celery
from Tickets import Tickets
from mongo_data_manager import MongoDataManager


# Create Celery object:
CELERY_BROKER = os.environ['CELERY_BROKER']
CELERY_BACKEND = os.environ['CELERY_BACKEND']
app = Celery('tasks', backend=CELERY_BACKEND, broker=CELERY_BROKER)


# Create Tickets object:
# By doing this we ensure that the layered architecture is respected:
MDM = MongoDataManager(uri=os.environ['DB_URI'], database='TicketsDB', collection='tickets')
tickets = Tickets(data_manager=MDM)


# Define celery task for purchase a ticket:
@app.task
def get_ticket(buyer_data, event_data):
    return tickets.buy_ticket(buyer_data, event_data)