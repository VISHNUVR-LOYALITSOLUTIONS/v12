# -*- coding: utf-8 -*-

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import models, fields, api
# import cStringIO
from io import BytesIO
import xlwt
from datetime import datetime
import base64

class GSTRHSNWizard(models.TransientModel):
    _name = 'invoice.report.gstrhsn.wizard'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')
    inv_type = fields.Selection([('gstr1', 'GSTR1'), ('gstr2', 'GSTR2')],
                             default='gstr1',string='GST Type')
    report = fields.Binary('Prepared file', filters='.xls', readonly=True)
    name = fields.Char('File Name', size=128)

    sorted_invoices = []
    pos_sorted_orders = []

    def get_valid_invoices(self):
        # Searching for customer invoices
        from_date = datetime.strptime(str(self.date_from), '%Y-%m-%d').date()
        to_date = datetime.strptime(str(self.date_to), '%Y-%m-%d').date()

        if self.inv_type == 'gstr1':
           inv_domain = ('type', 'in', ('out_invoice', 'out_refund'))
        else:
           inv_domain = ('type', 'in', ('in_invoice', 'in_refund'))

        # Get all invoices
        all_invoices = self.env['account.invoice'].search(
            [('date_invoice', '>=', from_date), ('date_invoice', '<=', to_date),('state', 'in', ['paid', 'open']),inv_domain])


        self.sorted_invoices = all_invoices.sorted(key=lambda p: (p.date_invoice, p.number))

        if self.inv_type == 'gstr1':

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
    def generate_gstrhsn_report(self):
        # Error handling is not taken into consideraion
        self.ensure_one()
        fp = BytesIO()
        xl_workbook = xlwt.Workbook(encoding='utf-8')

        from_date = datetime.strptime(str(self.date_from), '%Y-%m-%d').date()
        to_date = datetime.strptime(str(self.date_to), '%Y-%m-%d').date()

        # Get the invoices
        self.get_valid_invoices()

        self.generate_hsn_report(xl_workbook)

        xl_workbook.save(fp)

        out = base64.encodestring(fp.getvalue())
        self.write({'state': 'get',
                    'report': out,
                    'name': 'gstr1hsn_' + str(from_date) + '-' + str(to_date) + '.xls' if self.inv_type == 'gstr1' else 'gstr2hsn_' + str(from_date) + '-' + str(to_date) + '.xls'
                    })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.report.gstrhsn.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    """ GSTR-HSN Summary """

    def generate_hsn_report(self, wb1):
        # Error handling is not taken into consideraion
        self.ensure_one()

        ws1 = wb1.add_sheet('GSTR-HSN')
        fp = BytesIO()

        # Content/Text style
        header_content_style = xlwt.easyxf("font: name Arial size 12 px, bold 1, height 170;")
        sub_header_style = xlwt.easyxf("font: name Arial size 10 px, bold 1, height 170; align: horiz center")
        sub_header_content_style = xlwt.easyxf("font: name Arial size 10 px, height 170;")
        line_content_style = xlwt.easyxf("font: name Arial, height 170;")
        row = 1
        col = -1
        ws1.row(row).height = 500
        if self.inv_type == 'gstr1':
            ws1.write_merge(row, row, col + 1, col + 6, "GSTR1-HSN", header_content_style)
        else:
            ws1.write_merge(row, row, col + 1, col + 6, "GSTR2-HSN", header_content_style)
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
        ws1.write(row, col + 1, "HSN", sub_header_style)
        ws1.write(row, col + 2, "Description", sub_header_style)
        ws1.write(row, col + 3, "UQC", sub_header_style)
        ws1.write(row, col + 4, "Total Quantity", sub_header_style)
        ws1.write(row, col + 5, "Total Value", sub_header_style)
        ws1.write(row, col + 6, "Taxable Value", sub_header_style)
        ws1.write(row, col + 7, "Integrated Tax Amount", sub_header_style)
        ws1.write(row, col + 8, "Central Tax Amount", sub_header_style)
        ws1.write(row, col + 9, "State/UT Tax Amount", sub_header_style)
        ws1.write(row, col + 10, "Cess Amount", sub_header_style)

        hsn_summary_data = {}
        pd_list = []
        # configs=self.env['pos.config'].search([('active','=',True)])
        # for config in configs:
        #     pd_list.append(config.discount_product_id_cash)
        #     pd_list.append(config.discount_product_id)
        for invoice in self.sorted_invoices:
            for invoice_line in invoice.invoice_line_ids:
                prod_id = invoice_line.product_id
                if prod_id in pd_list:
                    continue
                line_uom = invoice_line.uom_id

                line_amount = invoice_line.price_subtotal_signed

                if invoice_line.discount:
                    price = invoice_line.price_unit * (1 - (invoice_line.discount or 0.0) / 100.0)
                else:
                    price = invoice_line.price_unit

                if invoice_line.invoice_id.inclusive:
                    line_taxes = invoice_line.invoice_line_tax_ids.with_context(price_include=True,
                                                                   include_base_amount=True).compute_all_inc(price,
                                                                                                             invoice_line.invoice_id.currency_id,
                                                                                                             invoice_line.quantity,
                                                                                                             product=prod_id,
                                                                                                             partner=invoice_line.invoice_id.partner_id)
                else:
                    line_taxes = invoice_line.invoice_line_tax_ids.compute_all(price,
                                                                           invoice_line.invoice_id.currency_id,
                                                                           invoice_line.quantity, prod_id,
                                                                           invoice_line.invoice_id.partner_id)

                if line_taxes:
                    line_amount = round(line_taxes['total_excluded'], 2) if invoice.type in ('out_invoice', 'in_invoice') else (
                        round((line_taxes['total_excluded'] * -1), 2))

                #_logger.info(line_taxes)
                igst_amount = cgst_amount = sgst_amount = cess_amount = gst_amount = kfc_amount = 0.0
                for tax_line in line_taxes['taxes']:
                    tax_obj = self.env['account.tax'].browse(tax_line['id'])
                    if invoice.partner_id.x_gstin:
                        if invoice.partner_id.x_gstin[0:2] == invoice.company_id.x_gstin[0:2]:
                            if tax_obj.cess:
                                cess_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                                        tax_line['amount'] * -1)
                            elif tax_obj.kfc:
                                kfc_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                                        tax_line['amount'] * -1)
                            else:
                                gst_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                                        tax_line['amount'] * -1)
                        else:
                            if tax_obj.cess:
                                cess_amount += tax_line['amount'] if invoice.type in (
                                'out_invoice', 'in_invoice') else (
                                        tax_line['amount'] * -1)
                            elif tax_obj.kfc:
                                kfc_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                                        tax_line['amount'] * -1)
                            else:
                                igst_amount += tax_line['amount'] if invoice.type in (
                                'out_invoice', 'in_invoice') else (
                                        tax_line['amount'] * -1)
                    else:
                        if invoice.partner_id.state_id.id == invoice.company_id.state_id.id:
                            if tax_obj.cess:
                                cess_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                                        tax_line['amount'] * -1)
                            elif tax_obj.kfc:
                                kfc_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                                        tax_line['amount'] * -1)
                            else:
                                gst_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                                        tax_line['amount'] * -1)
                        else:
                            if tax_obj.cess:
                                cess_amount += tax_line['amount'] if invoice.type in (
                                'out_invoice', 'in_invoice') else (
                                        tax_line['amount'] * -1)
                            elif tax_obj.kfc:
                                kfc_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                                    tax_line['amount'] * -1)
                            else:
                                igst_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                                    tax_line['amount'] * -1)

                    # if tax_obj.cess:
                    #     cess_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                    #                 tax_line['amount'] * -1)
                    # elif tax_obj.igst:
                    #     igst_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                    #                 tax_line['amount'] * -1)
                    # elif tax_obj.kfc:
                    #     kfc_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                    #                 tax_line['amount'] * -1)
                    # else:
                    #     gst_amount += tax_line['amount'] if invoice.type in ('out_invoice', 'in_invoice') else (
                    #                 tax_line['amount'] * -1)
                line_total_amount = line_amount + igst_amount + gst_amount + cess_amount + kfc_amount
                if line_total_amount > 0 and invoice.type in ('in_refund', 'out_refund'):
                    line_total_amount = line_total_amount * -1

                if invoice_line.quantity > 0 and invoice.type in ('in_refund', 'out_refund'):
                    line_qty = invoice_line.quantity * -1
                elif invoice_line.quantity >0 and invoice.type in ('out_invoice') and line_total_amount<0:
                    line_qty = invoice_line.quantity * -1
                else:
                    line_qty = invoice_line.quantity


                if hsn_summary_data.get(prod_id):
                    hsn_summary_data[prod_id][0] += line_qty
                    hsn_summary_data[prod_id][1] += line_total_amount
                    hsn_summary_data[prod_id][2] += line_amount
                    hsn_summary_data[prod_id][3] += igst_amount
                    hsn_summary_data[prod_id][4] += gst_amount/2
                    hsn_summary_data[prod_id][5] += gst_amount/2
                    hsn_summary_data[prod_id][6] += cess_amount
                else:
                    hsn_summary_data[prod_id] = [line_qty, line_total_amount, line_amount, igst_amount, gst_amount/2, gst_amount/2, cess_amount]

        # if self.inv_type == 'gstr1':
        #     for pos in self.pos_sorted_orders:
        #         for pos_line in pos.lines:
        #             prod_id = pos_line.product_id
        #             if prod_id in pd_list:
        #                 continue
        #             line_uom = prod_id.uom_id
        #             if (pos_line.price_subtotal < 0 and pos_line.qty < 0) or (pos_line.price_subtotal>=0 and pos_line.qty>=0):
        #                 line_qty = pos_line.qty
        #             elif pos_line.price_subtotal<0 and pos_line.qty >0:
        #                 line_qty = pos_line.qty*-1
        #             else:
        #                 line_qty = pos_line.qty
        #             line_amount = pos_line.price_subtotal
        #
        #             line_taxes = pos_line.tax_ids_after_fiscal_position.compute_all(pos_line.price_unit,
        #                                                           pos_line.order_id.pricelist_id.currency_id,
        #                                                           pos_line.qty, prod_id,
        #                                                           pos_line.order_id.partner_id)
        #             if line_taxes:
        #                 line_amount = round(line_taxes['total_excluded'], 2)
        #             igst_amount = cgst_amount = sgst_amount = cess_amount = gst_amount = kfc_amount = 0.0
        #             for tax_line in line_taxes['taxes']:
        #                 tax_obj = self.env['account.tax'].browse(tax_line['id'])
        #                 if pos.partner_id.x_gstin :
        #                     if pos.partner_id.x_gstin[0:2]==pos.company_id.x_gstin[0:2]:
        #                         if tax_obj.cess:
        #                             cess_amount += tax_line['amount']
        #                         elif tax_obj.kfc:
        #                             kfc_amount += tax_line['amount']
        #                         else:
        #                             gst_amount += tax_line['amount']
        #                     else:
        #                         if tax_obj.cess:
        #                             cess_amount += tax_line['amount']
        #                         elif tax_obj.kfc:
        #                             kfc_amount += tax_line['amount']
        #                         else:
        #                             igst_amount += tax_line['amount']
        #                 else:
        #                     if pos.partner_id.state_id.id == pos.company_id.state_id.id:
        #                         if tax_obj.cess:
        #                             cess_amount += tax_line['amount']
        #                         elif tax_obj.kfc:
        #                             kfc_amount += tax_line['amount']
        #                         else:
        #                             gst_amount += tax_line['amount']
        #                     else:
        #                         if tax_obj.cess:
        #                             cess_amount += tax_line['amount']
        #                         elif tax_obj.kfc:
        #                             kfc_amount += tax_line['amount']
        #                         else:
        #                             igst_amount += tax_line['amount']
        #             line_total_amount = line_amount + igst_amount + gst_amount + cess_amount + kfc_amount
        #             if hsn_summary_data.get(prod_id):
        #                 hsn_summary_data[prod_id][0] += line_qty
        #                 hsn_summary_data[prod_id][1] += line_total_amount
        #                 hsn_summary_data[prod_id][2] += line_amount
        #                 hsn_summary_data[prod_id][3] += igst_amount
        #                 hsn_summary_data[prod_id][4] += gst_amount / 2
        #                 hsn_summary_data[prod_id][5] += gst_amount / 2
        #                 hsn_summary_data[prod_id][6] += cess_amount
        #             else:
        #                 hsn_summary_data[prod_id] = [line_qty, line_total_amount, line_amount, igst_amount, gst_amount/2,
        #                                              gst_amount/2, cess_amount]
        # Can't sort dictionary, but get ordered list of tuples
        for product_hsn, hsn_sum in sorted(hsn_summary_data.items(), key=lambda p: p[0].name):

            row += 1
            uqc = 'OTH-OTHERS'
            if product_hsn.uom_id:
                uom = product_hsn.uom_id.id
                uqcObj = self.env['uom.mapping'].search([('uom', '=', uom)])
                if uqcObj:
                    uqc = uqcObj[0].name.code
            ws1.write(row, col + 1, product_hsn.hsn, line_content_style)
            ws1.write(row, col + 2, product_hsn.name, line_content_style)
            ws1.write(row, col + 3, uqc, line_content_style)
            # Quantity in Base UoM
            ws1.write(row, col + 4, hsn_sum[0], line_content_style)
            # Amount
            ws1.write(row, col + 5, hsn_sum[1], line_content_style)
            ws1.write(row, col + 6, hsn_sum[2], line_content_style)
            ws1.write(row, col + 7, hsn_sum[3], line_content_style)
            ws1.write(row, col + 8, hsn_sum[4], line_content_style)
            ws1.write(row, col + 9, hsn_sum[5], line_content_style)
            ws1.write(row, col + 10, hsn_sum[6], line_content_style)

    def format_date(self, date_in):
        return datetime.strftime(datetime.strptime(str(date_in), DEFAULT_SERVER_DATE_FORMAT), "%d/%m/%Y")