# -*- coding: utf-8 -*-
#
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError


class Picking(models.Model):
    _inherit = 'stock.picking'

# rule setting with curresponding to the operating unit select rule and amount
    @api.multi
    def action_confirm(self):
        res = super(Picking, self).action_confirm()
        for i in self:
            lines=[]
            branch_rule = i.operating_unit_id.select_rule.short_code
            branch_amount = i.operating_unit_id.branch_limit
            product = self.env['product.product'].search([])
            current_stock =0
            # current_st=0
            if branch_rule=='BSP':

                query = '''

                                           (select product_id as id,location_id as location_id,round(sum(name),4) as opening_stock from
                              (select i.id , l.id as location_id,product_id,i.name as description,
                                  case when state ='done' then product_qty else 0 end as name,
                                  case when state !='done' then product_qty else 0 end as product_qty_pending,date,picking_id,l.company_id
                              from stock_location l,
                                  stock_move i
                              where l.usage='internal'
                                  and i.location_dest_id = l.id
                                  and state != 'cancel'
                                  and i.company_id = l.company_id
                                  and l.operating_unit_id =%s

                              union all

                              select -o.id ,l.id as location_id ,product_id,o.name as description,
                                  case when state ='done' then -product_qty else 0 end as name,
                                  case when state !='done' then -product_qty else 0 end as product_qty_pending,date, picking_id,l.company_id
                              from stock_location l,
                                  stock_move o
                              where l.usage='internal'
                                  and o.location_id = l.id
                                  and state != 'cancel'
                                  and o.company_id = l.company_id
                                  and l.operating_unit_id=%s
                                  )s where location_id=%s group by product_id,location_id)
                          '''

                self.env.cr.execute(query, (i.operating_unit_id.id, i.operating_unit_id.id,i.location_dest_id.id))

                for row in self.env.cr.dictfetchall():


                    product_id = row['id'] if row['id'] else 0
                    opening_stock = row['opening_stock'] if row['opening_stock'] else 0

                    query3 = """
                    
                    select pt.list_price as sale_price from product_product as p 
        	left join product_template as pt on pt.id=p.product_tmpl_id 	
                                             where p.id=%s 

                                                  """

                    self.env.cr.execute(query3, (row['id'],))

                    closingstock_cost = 0
                    for ans1 in self.env.cr.dictfetchall():
                        closingstock_cost = ans1['sale_price'] if ans1['sale_price'] else 0

                    res = {
                        'id': row['id'],

                        'opening_stock': round(opening_stock, 2),
                        'current_stock': round((opening_stock * closingstock_cost), 2),
                    }
                    lines.append(res)

                current_stock = sum([item['current_stock'] for item in lines])
                # current_stock = sum([amount.qty_available * amount.lst_price for amount in product])
                current_product_stock = sum([am.qty_available * am.lst_price for ams in i.move_ids_without_package for am in ams.product_id])
                stock_form_product_stock = sum([am.product_uom_qty * am.product_id.lst_price for ams in i.move_ids_without_package for am in ams])

                if (branch_amount-current_stock) < stock_form_product_stock:

                    raise UserError(_('Your Transaction Limit Is %s') % (branch_amount-current_stock))


            elif branch_rule == 'BCP':


                query='''
                
                                (select product_id as id,location_id as location_id,round(sum(name),4) as opening_stock from
                              (select i.id , l.id as location_id,product_id,i.name as description,
                                  case when state ='done' then product_qty else 0 end as name,
                                  case when state !='done' then product_qty else 0 end as product_qty_pending,date,picking_id,l.company_id
                              from stock_location l,
                                  stock_move i
                              where l.usage='internal'
                                  and i.location_dest_id = l.id
                                  and state != 'cancel'
                                  and i.company_id = l.company_id
                                  and l.operating_unit_id =%s

                              union all

                              select -o.id ,l.id as location_id ,product_id,o.name as description,
                                  case when state ='done' then -product_qty else 0 end as name,
                                  case when state !='done' then -product_qty else 0 end as product_qty_pending,date, picking_id,l.company_id
                              from stock_location l,
                                  stock_move o
                              where l.usage='internal'
                                  and o.location_id = l.id
                                  and state != 'cancel'
                                  and o.company_id = l.company_id
                                  and l.operating_unit_id=%s
                                  )s where location_id=%s group by product_id,location_id)
                '''


                self.env.cr.execute(query, (i.operating_unit_id.id,i.operating_unit_id.id,i.location_dest_id.id))

                for row in self.env.cr.dictfetchall():


                    product_id = row['id'] if row['id'] else 0
                    opening_stock = row['opening_stock'] if row['opening_stock'] else 0



                    query3 = """
                    
                    
                    select ph.cost as cost from product_price_history as ph 
left join res_users as r on r.id = ph.write_uid where ph.product_id=%s and r.default_operating_unit_id=%s
order by ph.id DESC LIMIT 1

                                        """

                    self.env.cr.execute(query3, (row['id'],i.operating_unit_id.id))

                    closingstock_cost = 0
                    for ans1 in self.env.cr.dictfetchall():
                        closingstock_cost = ans1['cost'] if ans1['cost'] else 0

                    res = {
                        'id': row['id'],

                        'opening_stock': round(opening_stock, 2),
                        'current_stock': round((opening_stock * closingstock_cost), 2),
                    }
                    lines.append(res)


                current_stock = sum([item['current_stock'] for item in lines])

                # current_stock = sum([amount.qty_available * amount.standard_price for amount in product])
                current_product_stock = sum(
                    [am.qty_available * am.standard_price for ams in i.move_ids_without_package for am in ams.product_id])
                stock_form_product_stock = sum(
                    [am.product_uom_qty * am.product_id.standard_price for ams in i.move_ids_without_package for am in ams])

                if (branch_amount- current_stock) < stock_form_product_stock:
                    raise UserError(_('Your Transaction Limit Is %s') % (branch_amount-current_stock))

        return res


