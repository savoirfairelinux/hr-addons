.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

==================
Timesheet Employee
==================

Adds :
* is_timesheet to an analytic line, which makes this module relevant since this field was deleted in the community version of Odoo 10.0.
* employee to an analytic line which is also a timesheet, it corresponds to the unique employee linked to the user.
* product_id to an employee, hence the new account analaytic line amount computation.


Known issues / Roadmap
======================

* This module should not be added to the Enterprise version of Odoo 10.0 because the field is_timesheet already exists in it.
* The sale_timesheet module is not compatible, sale_timesheet auto_install must be False.  

Credits
=======

Contributors
------------

* Yasmine El Mrini <yasmine.elmrini@savoirfairelinux.com>
