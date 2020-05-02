#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import api, fields, models

class GstTaxData(models.TransientModel):
    _name = "gst.tax.data"

    def getTaxedAmount(self, rateObjs, price, currency, invoiceLineObj, invoiceObj):
        taxedAmount = 0.0
        total_excluded = 0.0
        if invoiceObj.inclusive:
            taxes = rateObjs.with_context(price_include=True,include_base_amount=True).\
                compute_all_inc(price,currency,invoiceLineObj.quantity,product=invoiceLineObj.product_id,
                        partner=invoiceObj.partner_id)
        else:
            taxes = rateObjs.compute_all(price,currency,invoiceLineObj.quantity,
                product=invoiceLineObj.product_id,partner=invoiceObj.partner_id)
        # taxes = rateObjs.compute_all(
        #     price,
        #     currency,
        #     invoiceLineObj.quantity,
        #     product=invoiceLineObj.product_id,
        #     partner=invoiceObj.partner_id
        # )
        if taxes:
            total_included = taxes.get('total_included') or 0.0
            total_excluded = taxes.get('total_excluded') or 0.0
            tax_details = taxes.get('taxes') or []
            taxedAmount = total_included - total_excluded
        if currency.name != 'INR':
            taxedAmount = taxedAmount * currency.rate
            total_excluded = total_excluded * currency.rate
        return [taxedAmount, total_excluded,tax_details]

    def getGstTaxData(self, invoiceObj, invoiceLineObj, rateObjs, taxedAmount, invoiceType):
        taxedAmount = round(taxedAmount, 2)
        gstDict = {
            "rt": 0.0, "iamt": 0.0, "camt": 0.0, "samt": 0.0, "csamt": 0.0
        }
        if invoiceType == "export":
            gstDict = {
                "txval": 0.0, "rt": 0, "iamt": 0.0
            }
        if invoiceType in ['imps', 'impg']:
            gstDict = {
                "elg": "no", "txval": 0.0, "rt": 0, "iamt": 0.0, 'tx_i': 0.0, 'tx_cs': 0.0
            }
        if invoiceType == "b2cs":
            gstDict['sply_ty'] = 'INTRA'
            gstDict['typ'] = 'OE'
        if rateObjs:
            if invoiceObj.partner_id.country_id.code == 'IN':
                for rateObj in rateObjs:
                    if rateObj.amount_type == "group":
                        for childObj in rateObj.children_tax_ids:
                            gstDict['rt'] = childObj.amount*2
                            gstDict['samt'] = round(taxedAmount/2, 2)
                            gstDict['camt'] = round(taxedAmount/2, 2)
                            break
                    else:
                        gstDict['rt'] = rateObj.amount
                        gstDict['iamt'] = round(taxedAmount, 2)
                    break
            elif invoiceType in ['imps', 'impg']:
                for rateObj in rateObjs:
                    gstDict['rt'] = rateObj.amount
                    gstDict['iamt'] = round(taxedAmount, 2)
                    break
        return gstDict