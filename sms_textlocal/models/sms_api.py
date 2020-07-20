# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.addons.iap.models import iap
import requests
DEFAULT_ENDPOINT = 'https://api.textlocal.in'
DEFAULT_SENDER = 'MaxVueTech'


class SmsApi(models.AbstractModel):
    _inherit = 'sms.api'
    @api.model
    def _send_sms(self, numbers, message):
        """ Send sms
        """
        apikey = self.env['iap.account'].get('textlocal')
        sender = self.env['ir.config_parameter'].sudo().get_param('textlocal.sender', DEFAULT_SENDER)
        params = {
            'apikey': apikey.account_token, 
			'message' : message,
			'sender': sender,
			'numbers': numbers
        }
        endpoint = self.env['ir.config_parameter'].sudo().get_param('textlocal.endpoint', DEFAULT_ENDPOINT)
        url = endpoint + '/send/?'
        r = requests.post(url=url, params=params)
        return True
        # ~ r = iap.jsonrpc(endpoint + '/send/?', params=params)
        # ~ print (params)
        # ~ print (endpoint)
        # ~ print (sender)
        # ~ print (apikey.account_token)
        # ~ print (url)
        # ~ print (r.status_code)
        # ~ print (r.text)
        
