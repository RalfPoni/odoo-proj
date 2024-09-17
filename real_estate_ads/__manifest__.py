{
    "name": "Real Estate Ads",
    "version": "1.0",
    "author": "Me",
    "description": """
            Testing description
    """,
    "category": "Marketing",
    "depends": ['base', 'mail'],
    "data": [
      'security/ir.model.access.csv',
        'security/res_groups.xml',

        'views/property_view.xml',
        'views/menu_items.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/property_offer_view.xml',

        # Data Files
        'data/property_type.xml',

        'report/property_report.xml',
        'report/report_template.xml',
    ],
    'assets' : {
        'web.assets_backend': [
            'real_estate_ads/static/src/js/my_custom_tag.js',
            'real_estate_ads/static/src/xml/my_custom_tag.xml'
        ]
    },
    "demo": [
        'demo/property_tag.xml'
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}