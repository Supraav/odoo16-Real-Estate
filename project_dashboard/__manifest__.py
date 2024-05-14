{
    'name': "Project Dashboard",
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
            'project_dashboard/static/src/**/**/*.js',
            'project_dashboard/static/src/**/**/*.xml',
            'project_dashboard/static/src/**/**/*.scss',
        ],
    },
}
