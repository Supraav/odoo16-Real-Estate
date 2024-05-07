{
    'name': "Awesome Tshirts",
    'version': '1.0',
    'depends': ['base','web'],
    'author': "Author Name",
    'description': """
        client action
        """,
    'application': True,
    'installable': True,
    'data':[
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'awesome_tshirts/static/src/**/**/*.js',
            'awesome_tshirts/static/src/**/**/*.xml',
            'awesome_tshirts/static/src/**/**/*.scss',
        ],
    },
}