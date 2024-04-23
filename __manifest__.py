# -*- coding: utf-8 -*-
{
    'name': "InstantAbode",

    'summary': """
        Simplifica el proceso de alquiler de inmuebles.
    """,

    'description': """
        InstantAbode es una aplicación diseñada para facilitar la gestión de alquileres de inmuebles, ofreciendo una plataforma intuitiva tanto para propietarios
        como para clientes. Los propietarios pueden agregar sus propiedades de manera sencilla, proporcionando detalles completos y atractivas descripciones para 
        atraer a posibles inquilinos. Por otro lado, los clientes tienen acceso a una amplia variedad de inmuebles disponibles para alquiler, con opciones 
        de búsqueda y filtros que les permiten encontrar fácilmente la propiedad que se ajuste a sus necesidades. Con un enfoque en la comodidad y la eficiencia,
        InstantAbode se esfuerza por ofrecer una experiencia fluida y personalizada para todos los usuarios, facilitando el proceso de alquiler de principio a fin.
    """,

    'author': "Esteve Asensio Meléndez",
    'website': "https://www.InstantAbode.es",

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
