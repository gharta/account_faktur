# -*- coding: utf-8 -*-
{
    'name': "Account Faktur",

    'summary': """
        Account Faktur Pajak""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Gharta Hadisa Halim",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_faktur_views.xml',
        'views/account_invoice_views.xml',
        'views/account_invoice_report.xml',
        'wizard/account_faktur_wizard_views.xml',
    ],
    'auto_install':True
}