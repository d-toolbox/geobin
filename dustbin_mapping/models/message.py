# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError
import requests
import json
from datetime import datetime
import time


class MapMessages(models.Model):
    _name = 'maps.messages'
    message_id = fields.Char('Message ID')
    phone = fields.Char('Phone')
    message = fields.Char('Message')
    date = fields.Date('Date Sent on Dcomposite')
    received = fields.Date('Date Received on GeoBin')

    _sql_constraints = [
        ('message_id_unique',
         'UNIQUE(message_id)',
         "The Message ID must be unique"),
    ]

    @api.model
    def _cron_get_messages(self):
        print "calling cron job >>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<"
        message_object = self.env['maps.messages']
        url = "http://104.197.248.134/api/v1/messages.json"
        header = {'Authorization': 'Token 88f6f60aa0db2e41354f833c8599db38589af8c5'}
        try:
            resp = requests.get(url, headers=header)
            messages = json.loads(resp.content)
            incoming = messages["results"]
        except:
            raise ValidationError("Failed Connecting to Dcomposite")

        needed = [mg for mg in incoming]
        for message in needed:
            if 10 > len(message["text"]) > 5:
                messages_in = self.env['maps.messages'].search([])
                message_id = message["id"]
                tel = message["urn"]
                text = message["text"]
                time_stamp = message["created_on"]
                if str(message_id) not in [str(msg.message_id) for msg in messages_in]:
                    message_object.create({
                        'message_id': message_id,
                        'phone': tel,
                        'message': text,
                        'date': time_stamp,
                        'received': datetime.now()
                    })
                else:
                    continue

        print "Generating Dustbin Status >>>>>>>>>><<<<<<<<<"
        messages = self.env['maps.messages'].search([])
        codes = self.env['dustbin.code'].search([])
        looped_obj = self.env['message.looped']
        for msg in messages:
            if msg.message:
                looped = self.env['message.looped'].search([])
                if msg.message_id not in [loop.name for loop in looped]:
                    code = ''
                    stat = ''
                    code_lower = [cod.name.lower() for cod in codes]
                    for s in ['empty', 'full']:
                        if s in msg.message.lower():
                            stat = s
                    for c in code_lower:
                        if c in msg.message.lower():
                            code = c
                    if len(code) > 1 and len(stat) > 1:
                        code_upper = code.upper()
                        dustbin = self.env['dustbin.dustbin'].search(
                            [('code', '=', code_upper)])
                        if dustbin:
                            dustbin.state = stat
                    looped_obj.create({
                        'name': msg.message_id,
                        'date': datetime.now()
                    })
                else:
                    continue

    @api.model
    def get_messages(self):
        print "calling manual get message >>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<"
        message_object = self.env['maps.messages']
        url = "http://104.197.248.134/api/v1/messages.json"
        header = {'Authorization': 'Token 88f6f60aa0db2e41354f833c8599db38589af8c5'}
        try:
            resp = requests.get(url, headers=header)
            messages = json.loads(resp.content)
            incoming = messages["results"]
        except:
            raise ValidationError("Failed Connecting to Dcomposite")
        needed = [mg for mg in incoming]
        print needed
        time.sleep(5)
        for message in needed:
            if 10 > len(message["text"]) > 5:
                messages_in = self.env['maps.messages'].search([])
                message_id = message["id"]
                tel = message["urn"]
                text = message["text"]
                time_stamp = message["created_on"]
                if str(message_id) not in [str(msg.message_id) for msg in messages_in]:
                    message_object.create({
                        'message_id': message_id,
                        'phone': tel,
                        'message': text,
                        'date': time_stamp,
                        'received': datetime.now()
                    })
                else:
                    continue

    @api.one
    def compute_dustbin_status(self):
        messages = self.env['maps.messages'].search([])
        codes = self.env['dustbin.code'].search([])
        looped_obj = self.env['message.looped']
        for msg in messages:
            if msg.message:
                looped = self.env['message.looped'].search([])
                if msg.message_id not in [loop.name for loop in looped]:
                    code = ''
                    stat = ''
                    code_lower = [cod.name.lower() for cod in codes]
                    for s in ['empty', 'full']:
                        if s in msg.message.lower():
                            stat = s
                    for c in code_lower:
                        if c in msg.message.lower():
                            code = c
                    if len(code) > 1 and len(stat) > 1:
                        code_upper = code.upper()
                        dustbin = self.env['dustbin.dustbin'].search(
                            [('code', '=', code_upper)])
                        if dustbin:
                            dustbin.state = stat
                    looped_obj.create({
                        'name': msg.message_id,
                        'date': datetime.now()
                    })
                else:
                    continue
