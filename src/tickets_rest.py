# -*- coding: utf-8 -*-

import os
import hug
from falcon import HTTP_200
from tickets_tasks import tickets, get_ticket, app


# Call the get ticket task:
@hug.post("/ticket")
def buy_ticket_request(body: hug.types.json, response):
    event_data = body['event']
    buyer_data = body['buyer']
    # Send task:
    task = get_ticket.delay(buyer_data, event_data)
    # Return task.id:
    response.satus = HTTP_200
    return task.id


# Get the response of the get ticket task:
@hug.get('/ticket/{task_id}', output=hug.output_format.file)
def buy_ticket_response(task_id, response):
    task_result = app.AsyncResult(task_id)
    response = HTTP_200
    return task_result.result


@hug.get("/ticket/isvalid/{ticket_id}")
def ticket_is_valid(ticket_id, response):
    out = tickets.is_valid(ticket_id)
    response = HTTP_200
    if out:
        return "The ticket is valid"
    else:
        return "The ticket is invalid"