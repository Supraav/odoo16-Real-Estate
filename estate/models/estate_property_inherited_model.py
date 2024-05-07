from odoo import fields,models,api
from datetime import datetime,timedelta
from odoo.exceptions import UserError,ValidationError

class EstatePropertyInheritedModel(models.Model):
    _inherit = 'res.users'

    property_ids=fields.One2many('estate.property','salesperson',string='',domain="['|',('state', '=', 'new'),('state', '=', 'offer_received')]")
    


