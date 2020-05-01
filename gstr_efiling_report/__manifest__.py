# -*- coding: utf-8 -*-
{
    'name': "gstr_efiling_report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','account_tax_python','uom', 'l10n_in',
        ],
    'data': [
        'data/ir_model_fields_data.xml',
        'data/port.code.csv',
        'data/data_unit_quantity_code.xml',
        'data/data_uom_mapping.xml',
        'security/gst_security.xml',
        'security/ir.model.access.csv',
        'wizard/message_wizard_view.xml',
        'wizard/invoice_type_wizard_view.xml',
        'data/account_data.xml',
        'data/account_tax_data.xml',
        'data/account_fiscal_position_data.xml',
        'data/res_country_state_data.xml',
        'views/account_financial_report_data.xml',
        'views/account_report.xml',
        'views/product_template_view.xml',
        'views/report_invoice.xml',
        'views/report_templates.xml',
        'views/res_company_view.xml',
        'views/res_country_state_view.xml',
        'wizard/account_report_tax_payable_view.xml',
        'data/gob_server_actions.xml',
        'views/account_invoice_view.xml',
        'views/gst_view.xml',
        'views/port_code_view.xml',
        'views/gstr2_view.xml',
        'views/res_partner_views.xml',

        'views/account_fiscalyear_view.xml',
        'views/ir_attachment_view.xml',
        'views/account_period_view.xml',
        'views/gst_sequence.xml',
        'views/unit_quantity_code_view.xml',
        'views/uom_map_view.xml',
        'views/gst_action_view.xml',
        'views/gst_menu_view.xml',

        'views/views.xml',
        'views/b2cl.xml',
        'views/b2cs.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}