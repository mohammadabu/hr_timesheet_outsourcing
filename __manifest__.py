# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'hr_timesheet_outsourcing',
    'version': '1.0',
    'depends': ['hr', 'analytic', 'outsourcing', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'views/outsourcing_views.xml',
        'views/outsourcing_portal_templates.xml',
    ],
    'demo': [
        
    ],
}
