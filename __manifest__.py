# -*- coding: utf-8 -*-
{
    'name': "InstantAbode",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Esteve Asensio",
    'website': "https://www.InstantAbode.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/cliente.xml',
        'views/propietario.xml',
        'views/valoracioncliente.xml',
        'views/valoracioninmueble.xml',
        'views/inmueble.xml',
        'views/alquiler.xml',
        'views/menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}
