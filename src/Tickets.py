# -*- coding: utf-8 -*-


import io
import uuid
import datetime
import treepoem
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


class Tickets:
    # Dependency injection:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        # Create a temporal directory for save generated files:
        self.tmp_dir = tempfile.mkdtemp()


    def buy_ticket(self, buyer_data, event_data):
        barcode, ticket_id = self.generate_barcode(event_data['_id'], buyer_data['name'])
        ticket = self.generate_ticket(buyer_data, event_data, barcode)
        # Create payment register:
        register = dict(
            owner_name=buyer_data['name'],
            owner_email=buyer_data['email'],
            buy_date=datetime.datetime.today(),
            ticket_id=ticket_id
        )
        # Store register:
        self.data_manager.insert(register)
        return ticket

    
    def is_valid(self, ticket_id):
        """ Check if certain ticket id is valid or not """
        return self.data_manager.get(key='ticket_id', value=ticket_id) != None


    def generate_ticket(self, buyer_data, event_data, barcode):
        file_name = self.tmp_dir + '/Ticket_' + uuid.uuid4().hex[:8] + '.pdf'
        c = canvas.Canvas(file_name)
        c.drawString(100,750,"Datos del comprador")
        c.drawString(130, 730, "Nombre: " + buyer_data['name'])
        c.drawString(130, 710, "Correo: " + buyer_data['email'])
        c.drawString(100, 660, "Datos del evento")
        c.drawString(130, 640, "Título: " + event_data['title'])
        c.drawString(130, 620, "Organizador: " + event_data['organizer'])
        c.drawString(130, 600, "Fecha y hora: " + str(event_data['date']))
        c.drawString(130, 580, "Dirección: " + event_data['address'])
        c.drawImage(barcode, 110, 400)
        c.save()
        return file_name


    def generate_barcode(self, event_id, buyer_name):
        ticket_id = uuid.uuid4().hex + '-' + event_id + '-' + buyer_name.replace(" ", "")
        image = treepoem.generate_barcode(barcode_type='qrcode', data=ticket_id)
        # Preprocess image to make it compatible with reportlab:
        _bytes = io.BytesIO()
        image.save(_bytes, format='png')
        _bytes.seek(0)
        barcode = ImageReader(_bytes)
        return barcode, ticket_id