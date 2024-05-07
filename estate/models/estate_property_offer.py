from odoo import fields,models,api
from datetime import datetime,timedelta
from odoo.exceptions import UserError,ValidationError

class EstatePropertyOffer(models.Model):
    _name='estate.property.offer'
    _description='estate property offer table'
    _order="price desc"

    price=fields.Float()
    status=fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')],copy=False)

    partner_id=fields.Many2one('res.partner',required=True,string="Partner")
    property_id=fields.Many2one('estate.property',required=True,string="property name")

    validity=fields.Integer(default=7)
    date_deadline=fields.Date(compute="_compute_date", inverse="_inverse_validity")

    property_type_id=fields.Many2one(related='property_id.property_type_id',store=True)    
    

    _sql_constraints = [
        ('check_offered_price', 'CHECK(price > 0)',
         'The offered price of the estate should be greater than 0.'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'The selling price of the estate should be greater than 0.')
    ]

    @api.depends("validity")
    def _compute_date(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline=offer.create_date.date() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = datetime.now().date() + timedelta(days=offer.validity)


    def _inverse_validity(self):
        if self.date_deadline:
            diff=self.date_deadline-self.create_date.date()
            self.validity=diff.days if diff.days >0 else 0

    def action_accept(self):
        for record in self:
            property=record.property_id

            if property.state=="offer_accepted":
                raise UserError("offer already accepted for this property")

            if property.state == "new" or property.state=="offer_received":
                property.selling_price= record.price
                property.buyer = record.partner_id
                record.status="accepted"
                property.state = 'offer_accepted' 
            else:
                raise UserError("You cannot Accept the offer.")
            
    def action_cancel(self):
        for record in self:
            property=record.property_id
            if record.status=="accepted" or property.state=="offer_accepted":
                raise UserError("Offer already Accepted!")
            else:
                record.status="refused"

    @api.model
    def create(self, vals):
        property_obj=self.env['estate.property']
        property_id=vals.get('property_id')
        property = property_obj.browse(property_id)
        property.state = 'offer_received'  

        existing_offers = self.search([('property_id', '=', property_id), ('price', '>', vals.get('price'))])
        if existing_offers:
            raise ValidationError("Cannot create an offer with a lower amount than an existing offer.")

        return super(EstatePropertyOffer, self).create(vals)
    