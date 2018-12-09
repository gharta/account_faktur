import base64
import functools
import json
import math
import werkzeug
from odoo import http, _, fields

class KampusController(http.Controller):
    
    @http.route('/api/get_siswa', methods=['GET'], type="http", auth="none", csrf=False, cors='*')
    def get_siswa(self, **kw):
        # self.env diganti dengan http.request.env
        invoices = http.request.env['account.invoice'].sudo().search([])
        siswa = http.request.env['kampus.siswa'].sudo().search([])
        # FROM siswa
        res = []
        for inv in invoices :
            res.append({
                'nomor' : inv.number,
                'partner' : inv.partner_id.name
            })

        return http.request.make_response(json.dumps(res), headers=[
                ('Content-Type', 'application/json'),
        ])