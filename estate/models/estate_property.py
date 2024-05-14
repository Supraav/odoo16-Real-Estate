from odoo import fields,models,api
from datetime import datetime,timedelta
from odoo.exceptions import UserError,ValidationError

class EstateProperty(models.Model):
    _name="estate.property"
    _description="estate property table"
    _order="id desc"
    
    name=fields.Char(required=True, translate=True)
    status=fields.Char()
    description=fields.Text(string="Description")
    postcode=fields.Char()
    date_availability=fields.Date(copy=False,default=datetime.today()+ timedelta(days=90))
    expected_price=fields.Float()
    selling_price=fields.Float(readonly=True,copy=False)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    active = fields.Boolean('Active',default=True)
    state=fields.Selection(
            selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')]
            ,required=True,copy=False,default="new")
    
    garden_orientation=fields.Selection(selection=[('north','north'),('south','south'),('east','east'),('west','west')])

    property_type_id=fields.Many2one("estate.property.type", string='Property')  

    salesperson=fields.Many2one('res.users',default=lambda self:self.env.user,string="Salesman",readonly=True)
    buyer=fields.Many2one('res.partner',string="Buyer")

    property_tag_ids=fields.Many2many('estate.property.tag',string='Property Tag')

    offer_ids=fields.One2many('estate.property.offer','property_id',string="offers")

    total_area=fields.Integer(compute="_compute_total")
    best_price=fields.Float(compute="_compute_best_price")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price of the estate should be greater than 0.'),

        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price of the estate should be greater than 0.'),
    ]

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        self.total_area=self.living_area+self.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        if self.offer_ids:
            self.best_price=max(self.offer_ids.mapped("price"))
        else:
            self.best_price=0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area=0
            self.garden_orientation=False

    def action_do_sold(self):
        if self.state=="canceled":
            raise UserError("Canceled user cannot be Sold")
        else:
            self.state="sold"


    def action_do_cancel(self):
        if self.state=="sold":
            raise UserError("Sold user cannot be Canceled")
        else:
            self.state="canceled"

    @api.constrains('selling_price','expected_price')
    def check_selling_price(self):
        for record in self:
            if (record.selling_price>0) and (record.selling_price<(0.9*record.expected_price)):
                raise UserError("selling price cannot be lower than 90% of the expected price.")
            
    @api.ondelete(at_uninstall=False)
    def delete_property(self):
        for record in self:
            if record.state=='new' or record.state=='canceled':
                return ("Property deleted successfully")
            else:
                raise UserError("Only new or canceled properties can be sold")
            
    @api.model
    def get_statistics(self):
        total_properties=self.search_count([])

        total_expected_price = sum(property.expected_price for property in self.search([]))
        average_expected_price = total_expected_price / total_properties if total_properties else 0

        total_sold_properties=self.search_count([('state','=','sold')])

        # property by type 
        property_types = self.env['estate.property.type'].search([])
        properties_by_type = {}
        for property_type in property_types:
            properties_count = self.search_count([('property_type_id', '=', property_type.id)])
            properties_by_type[property_type.name] = properties_count

        # property by tag 
        property_tags = self.env['estate.property.tag'].search([])
        properties_by_tag = {}
        for property_tag in property_tags:
            properties_tag_count = self.search_count([('property_tag_ids', '=', property_tag.id)])
            properties_by_tag[property_tag.name] = properties_tag_count


        # All the estates in asc order{bar graph }
        properties = self.search([], order='expected_price asc')
        property_names = [prop.name for prop in properties]
        property_expected_prices = [prop.expected_price for prop in properties]

        expected_price_distribution = {
            name: price for name, price in zip(property_names, property_expected_prices)
        }

        living_area_properties = self.search([], order='expected_price asc')
        living_area_property_names = [prop.name for prop in living_area_properties]
        living_area_property_prices = [prop.living_area for prop in properties]
        living_area_distribution = {
            name: price for name, price in zip(living_area_property_names, living_area_property_prices)
        }

        date_7_days_ago = datetime.today() - timedelta(days=7)
        total_sales_revenue = sum(property.selling_price for property in self.search([('state', '=', 'sold'), ('write_date', '>=', date_7_days_ago)]))
        
        return{
            'total_properties':total_properties,
            'average_expected_price':round(average_expected_price,3),
            'total_sold_properties': total_sold_properties,
            "properties_by_type": properties_by_type,
            "properties_by_tag": properties_by_tag,
            'expected_price_distribution': expected_price_distribution,
            'living_area_distribution': living_area_distribution,
            'total_sales_revenue_last_7_days': total_sales_revenue,
        }


# PROPERTY TYPE 
class EstatePropertyType(models.Model):
    _name='estate.property.type'
    _description='estate property type table'
    _order="sequence,name asc"

    name=fields.Char(required=True)

    property_ids = fields.One2many('estate.property', 'property_type_id')   

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    offer_ids=fields.One2many('estate.property.offer','property_type_id',string='offer ID')
    offer_count=fields.Integer(compute="_compute_offer_ids")

    _sql_constraints = [
        ('unique_type_name','UNIQUE(name)',
         'The property type name should be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offer_ids(self):
        for record in self:
            record.offer_count=len(record.offer_ids)


    def return_action_to_open(self):
        """ This opens the xml view specified in xml_id for the current vehicle """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:

            res = self.env['ir.actions.act_window']._for_xml_id(xml_id)
            res.update(
                context=dict(self.env.context, default_property_type_id=self.id, group_by=False),
                domain=[('property_type_id', '=', self.id)]
            )
            return res
        return False