from odoo import http
from odoo.http import request

class AwesomeTshirt(http.Controller):
    @http.route('/property/statistics', type='json', auth='user')
    def get_statistics(self):
        return http.request.env['estate.property'].get_statistics()