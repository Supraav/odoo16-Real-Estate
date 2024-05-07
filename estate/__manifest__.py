{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base','hr'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    'application': True,
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tags.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_inherited.xml',
    ]
}