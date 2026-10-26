=======================
Tag & Salesperson Sync
=======================

Overview
========

**Tag & Salesperson Sync** is an Odoo 18.0 module that keeps tags and the
Salesperson in step across Contacts, CRM and Sales.

In standard Odoo, Contacts, CRM and Sales each keep their own tags and their
own Salesperson, so the same information is entered again on every record.
This module removes that work through two options on the Company.

Features
========

* **Unify Lead & Contact Tags:** CRM tags and Contact tags share the same
  names. Creating or renaming a tag in one place does the same in the other.
* Duplicate tag names are not allowed across CRM and Contacts.
* Selecting a contact on a lead or opportunity adds the contact's tags to the
  lead automatically. Tags already on the lead are kept.
* **Use Contact Salesperson on Leads:** selecting a contact on a lead or
  opportunity sets the lead's Salesperson to the contact's Salesperson.
* With the Sales app installed, **New Quotation** on the opportunity creates a
  quotation with the same tags and the same Salesperson.
* Each option can be enabled separately, per company.
* When both options are off, Odoo behaves exactly as before.

Company Options
===============

==================================  ======================================================
Option                              What it does
==================================  ======================================================
Unify Lead & Contact Tags           Shares tags between CRM and Contacts and copies the
                                    contact's tags to the lead.
Use Contact Salesperson on Leads    Sets the lead's Salesperson from the selected contact.
==================================  ======================================================

The first time *Unify Lead & Contact Tags* is enabled, tags that exist only in
CRM or only in Contacts are created on the other side, so both lists match.

Installation
============

#. Copy the module folder into your Odoo addons path.
#. Restart the Odoo server.
#. Go to **Apps** and click **Update Apps List**.
#. Search for **Tag & Salesperson Sync** and click **Install**.

Usage
=====

#. Go to **Settings > Companies**, open your company and enable the options
   you need.
#. Create a tag in CRM or in Contacts. The matching tag is created on the
   other side.
#. Open a CRM lead or opportunity and select a contact. The contact's tags are
   added, and the Salesperson is taken from the contact.
#. Click **New Quotation** on the opportunity. The quotation has the same tags
   and Salesperson.

Support
=======

For support, contact: support@ninaadglobal.com

Author
======

**Ninaad Global Pvt Ltd.**
https://www.ninaadglobal.com
