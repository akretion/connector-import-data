connector-import-data
=====================

future versions
----------------
Use https://github.com/OCA/connector-interfaces/tree/8.0/base_import_async instead of this poc


connector buffer
------------------
Abstract Module that give the posibility to store a data and to
create a job to process it. Usefull for importing data using the
connector module.

connector base_import
---------------------

This module enhance base_import in order to run asynchronously and atomically imports.
It uses connector in order to create an import job by row from a csv file.
This module is working but it's for now a prototype, we may want to add the posibility to support mapping.
Also we plan to merge this module/feature with https://github.com/camptocamp/connector-file
