# -*- coding: utf-8 -*-

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools import float_is_zero
from odoo import models, fields, api
from io import BytesIO
import xlwt
from datetime import datetime
import base64

def _unescape(text):
    from urllib.parse import unquote_plus
    # from urllib import unquote_plus
    try:
        text = unquote_plus(text.encode('utf8'))
        return text
    except Exception as e:
        return text

class GSTRB2CSWizard(models.TransientModel):
    _name = 'invoice.report.kfc.wizard'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')

    report = fields.Binary('Prepared file', filters='.xls', readonly=True)
    name = fields.Char('File Name', size=128)

    sorted_invoices = []
    pos_sorted_orders = []

    def get_valid_invoices(self):
        # Searching for customer invoices
        from_date = datetime.strptime(str(self.date_from), '%Y-%m-%d').date()
        to_date = datetime.strptime(str(self.date_to), '%Y-%m-%d').date()

        # Get all invoices
        all_invoices = self.env['account.invoice'].search(
            [('date_invoice', '>=', from_date), ('date_invoice', '<=', to_date),('state', 'in', ['paid', 'open']),('type', '=', 'out_invoice')])



        self.sorted_invoices = all_invoices.sorted(key=lambda p: (p.date_invoice, p.number))


        filter = [
            ('date_order', '>=', fields.Datetime.to_string(
                datetime.combine(from_date, datetime.min.time()))),
            ('date_order', '<=', fields.Datetime.to_string(
                datetime.combine(to_date, datetime.max.time()))),
            ('state', 'in', ['paid', 'done']),
        ]

        # pos_order_objects = self.env['pos.order'].search(filter)
        #
        # self.pos_sorted_orders = pos_order_objects.sorted(key=lambda p: (p.date_order, p.name))




    @api.multi
    def generate_gstrsale_report(self):
        # Error handling is not taken into consideraion
        self.ensure_one()
        fp = BytesIO()
        xl_workbook = xlwt.Workbook(encoding='utf-8')

        from_date = datetime.strptime(str(self.date_from), '%Y-%m-%d').date()
        to_date = datetime.strptime(str(self.date_to), '%Y-%m-%d').date()

        # Get the invoices
        self.get_valid_invoices()

        self.generate_kfc_report(xl_workbook)

        xl_workbook.save(fp)

        out = base64.encodestring(fp.getvalue())
        self.write({'state': 'get',
                    'report': out,
                    'name': 'kfc' + str(from_date) + '-' + str(to_date) + '.xls'
                    })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.report.kfc.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    """ GSTR-1 B2CS Summary """

    def generate_kfc_report(self, wb1):
        # Error handling is not taken into consideraion
        self.ensure_one()

        ws1 = wb1.add_sheet('KFC')
        fp = BytesIO()

        # Content/Text style
        header_content_style = xlwt.easyxf("font: name Arial size 12 px, bold 1, height 170;")
        sub_header_style = xlwt.easyxf("font: name Arial size 10 px, bold 1, height 170; align: horiz center")
        sub_header_content_style = xlwt.easyxf("font: name Arial size 10 px, height 170;")
        line_content_style = xlwt.easyxf("font: name Arial, height 170;")
        row = 1
        col = -1
        ws1.row(row).height = 500
        ws1.write_merge(row, row, col + 1, col + 6, "KFC", header_content_style)

        row += 2
        ws1.write(row, col + 1, "From:", sub_header_style)
        ws1.write(row, col + 2, self.format_date(self.date_from), sub_header_content_style)
        row += 1
        ws1.write(row, col + 1, "To:", sub_header_style)
        ws1.write(row, col + 2, self.format_date(self.date_to), sub_header_content_style)
        row += 1
        ws1.write(row, col + 1, "GSTIN", sub_header_style)
        ws1.write(row, col + 2, self.env.user.company_id.x_gstin, sub_header_content_style)
        row += 1
        ws1.write(row, col + 1, "Legal name of the registered person", sub_header_style)
        ws1.write(row, col + 2, self.env.user.company_id.name, sub_header_content_style)
        row += 1

        ws1.write(row, col + 1, "Place Of Supply", sub_header_style)
        ws1.write(row, col + 2, "Taxable Value", sub_header_style)
        ws1.write(row, col + 3, "Rate", sub_header_style)
        ws1.write(row, col + 4, "GST Amount", sub_header_style)
        ws1.write(row, col + 5, "KFC Rate", sub_header_style)
        ws1.write(row, col + 6, "KFC Amount", sub_header_style)
        ws1.write(row, col + 7, "Cess Amount", sub_header_style)
        ws1.write(row, col + 8, "Total", sub_header_style)

        row += 1

        grouped_tax_lines = {}

        for invoice in self.sorted_invoices.filtered(
                lambda p: not p.partner_id.x_gstin and p.partner_id.country_id.code == 'IN'):  # GST registered customers

            amount_total = invoice.amount_total_signed
            if invoice.currency_id.name != 'INR':
                amount_total = amount_total * invoice.currency_id.rate
            if amount_total >= 250000 and invoice.partner_id.state_id.code != invoice.company_id.state_id.code:
                continue


            for invoice_line in invoice.invoice_line_ids:
                if invoice.inclusive:
                    line_taxes = invoice_line.invoice_line_tax_ids.with_context(price_include=True, include_base_amount=True).\
                        compute_all_inc(invoice_line.price_unit,invoice.currency_id,
                                    invoice_line.quantity,invoice_line.product_id,
                                    invoice.partner_id)
                else:
                    line_taxes = invoice_line.invoice_line_tax_ids.compute_all(invoice_line.price_unit, invoice.currency_id,
                                                                           invoice_line.quantity,
                                                                           invoice_line.product_id, invoice.partner_id)

                state = invoice.partner_id.state_id
                code = state.x_tin or 0
                code = _unescape(state.x_tin)
                sname = _unescape(state.name)
                stateName = "{}-{}".format(code, sname)
                rate = 0.0
                gstDict = {
                    "rt": 0.0, "iamt": 0.0, "gst": 0.0, "csamt": 0.0, "kfc": 0.0, "kfc_rate": 0.0, "kfc_count": 0.0
                }
                if invoice_line.invoice_line_tax_ids:
                    for rateObj in invoice_line.invoice_line_tax_ids:
                        if rateObj.amount_type == "group":
                            for childObj in rateObj.children_tax_ids:
                                if not childObj.cess and not childObj.kfc:
                                    rate = childObj.amount * 2
                                    break
                        else:
                            rate = rateObj.amount


                    for tax in line_taxes['taxes']:
                        tax_obj = self.env['account.tax'].browse(tax['id'])
                        if tax_obj.cess:
                            gstDict['csamt'] += tax['amount']
                        if tax_obj.kfc:
                            gstDict['kfc'] += tax['amount']
                            gstDict['kfc_rate'] += tax_obj.amount
                            gstDict['kfc_count'] += 1
                        elif tax_obj.igst:
                            gstDict['iamt'] += tax['amount']
                            gstDict['rt'] = tax_obj.amount
                        elif tax_obj.cess == False and tax_obj.igst == False and tax_obj.kfc == False:
                            gstDict['gst'] += tax['amount']
                            gstDict['rt'] += tax_obj.amount


                if grouped_tax_lines.get(stateName):
                    if grouped_tax_lines[stateName].get(rate):
                        grouped_tax_lines[stateName][rate][0] += line_taxes['total_excluded']
                        grouped_tax_lines[stateName][rate][1] += gstDict['gst'] + gstDict['iamt']
                        grouped_tax_lines[stateName][rate][2] += gstDict['kfc_rate']
                        grouped_tax_lines[stateName][rate][3] += gstDict['kfc']
                        grouped_tax_lines[stateName][rate][4] += gstDict['csamt']
                        grouped_tax_lines[stateName][rate][5] += line_taxes['total_included']
                        grouped_tax_lines[stateName][rate][6] += gstDict['kfc_count']
                    else:
                        grouped_tax_lines[stateName][rate] = [0, 0, 0, 0, 0, 0, 0]
                        grouped_tax_lines[stateName][rate][0] = line_taxes['total_excluded']
                        grouped_tax_lines[stateName][rate][1] = gstDict['gst'] + gstDict['iamt']
                        grouped_tax_lines[stateName][rate][2] = gstDict['kfc_rate']
                        grouped_tax_lines[stateName][rate][3] = gstDict['kfc']
                        grouped_tax_lines[stateName][rate][4] = gstDict['csamt']
                        grouped_tax_lines[stateName][rate][5] = line_taxes['total_included']
                        grouped_tax_lines[stateName][rate][6] += gstDict['kfc_count']
                else:
                    grouped_tax_lines[stateName] = {rate: [0, 0, 0, 0, 0, 0, 0]}
                    grouped_tax_lines[stateName][rate][0] = line_taxes['total_excluded']
                    grouped_tax_lines[stateName][rate][1] = gstDict['gst'] + gstDict['iamt']
                    grouped_tax_lines[stateName][rate][2] = gstDict['kfc_rate']
                    grouped_tax_lines[stateName][rate][3] = gstDict['kfc']
                    grouped_tax_lines[stateName][rate][4] = gstDict['csamt']
                    grouped_tax_lines[stateName][rate][5] = line_taxes['total_included']
                    grouped_tax_lines[stateName][rate][6] += gstDict['kfc_count']



        for place_of_supply, inv_tax_lines in grouped_tax_lines.items(): # invoice_gst_tax_lines.items():
            for tax_id, base_amount in inv_tax_lines.items():

                ws1.write(row, col + 1, place_of_supply, line_content_style)
                ws1.write(row, col + 2, base_amount[0], line_content_style)
                ws1.write(row, col + 3, tax_id, line_content_style)
                ws1.write(row, col + 4, base_amount[1], line_content_style)
                ws1.write(row, col + 5, base_amount[2]/base_amount[6] if base_amount[6] else 0, line_content_style)
                ws1.write(row, col + 6, base_amount[3], line_content_style)
                ws1.write(row, col + 7, base_amount[4], line_content_style)
                ws1.write(row, col + 8, base_amount[5], line_content_style)

                row += 1


    def format_date(self, date_in):
        return datetime.strftime(datetime.strptime(str(date_in), DEFAULT_SERVER_DATE_FORMAT), "%d/%m/%Y")