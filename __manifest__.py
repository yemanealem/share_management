{
    'name': 'Share Management',
    'version': '1.0',
    'summary': 'Manage shareholders, shares, dividends, and transactions',
    'category': 'Accounting',
    'author': 'YourName',
    'depends': ['base', 'mail'],
    'data': [


        'security/share_management_security.xml',
         'security/ir.model.access.csv',
        'views/shareholder_views.xml',
        'views/share_transaction_views.xml',
        
    ],
    'installable': True,
    'application': True,
}
