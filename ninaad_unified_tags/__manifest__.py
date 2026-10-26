{
    'name': 'Tag & Salesperson Sync',
    'version': '18.0.1.0.0',
    'summary': 'Share tags between Contacts, CRM and Quotations and copy the '
               'contact Salesperson to CRM leads, using two Company options',
    'description': """
Tag & Salesperson Sync
======================
In standard Odoo, Contacts, CRM and Sales each keep their own tags and their
own Salesperson. This module keeps them in step through two options on the
Company.

Unify Lead & Contact Tags
-------------------------
When enabled for a company:

    - CRM tags (crm.tag) and Contact tags (res.partner.category) share the
      same names. Creating or renaming a tag in one place does the same in
      the other.
    - Duplicate tag names are not allowed across CRM and Contacts.
    - Selecting a contact on a lead or opportunity adds the contact's tags
      to the lead automatically. Tags already on the lead are kept.

Use Contact Salesperson on Leads
--------------------------------
When enabled for a company:

    - Selecting a contact on a lead or opportunity sets the lead's
      Salesperson to the contact's Salesperson.

Quotations
----------
With the Sales app installed, "New Quotation" on the opportunity creates a
quotation with the same tags and the same Salesperson as the opportunity.

Each option can be enabled separately. When both options are off, Odoo
behaves exactly as before.
""",
    'category': 'CRM',
    'author': 'Ninaad Global Pvt Ltd.',
    'website': 'https://www.ninaadglobal.com',
    'support': 'support@ninaadglobal.com',
    'depends': ['base', 'crm'],
    'data': ['views/res_company_views.xml'],
    'images': ['static/description/screen_image.png'],
    'license': 'Other proprietary',
    'installable': True,
    'application': False,
}
