{
    'name': "Custom Dashboard",
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
            'client_actions/static/src/**/**/*.js',
            'client_actions/static/src/**/**/*.xml',
            'client_actions/static/src/**/**/*.scss',
        ],
    },
}