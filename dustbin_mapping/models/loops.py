from openerp import models, fields
from datetime import datetime


class LoopedId(models.Model):
    _name = 'message.looped'
    name = fields.Char("Loop ID")
    date = fields.Date(default=datetime.now())