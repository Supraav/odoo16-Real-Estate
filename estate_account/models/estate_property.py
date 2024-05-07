from odoo import fields,models,api

class EstateProperty(models.Model):
    _inherit='estate.property'

    def action_do_sold(self):
        res = super().action_do_sold()
        self.env['account.move'].create(
            {
                'partner_id':self.buyer.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': 
                [
                    (0,0,{
                        "name": "Property 6% selling price",
                        "quantity":1,
                        "price_unit": self.selling_price
                    }),

                    (0,0,{
                        "name": "Administrative fees",
                        "quantity":1,
                        "price_unit": 100

                    })
                ]
            }
        )      
        return res
    