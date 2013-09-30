# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2013 Akretion (http://www.akretion.com).
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


from openerp.osv import orm
from openerp.addons.connector.queue.job import job
from openerp.addons.connector.session import ConnectorSession


CONNECTOR_IMPORT_KEY = 'connector_import'


class connector_base_import_installed(orm.AbstractModel):
    _name = 'connector_base_import.connector'


class connector_base_import(orm.TransientModel):
    _inherit = 'base_import.import'

    def do(self, cr, uid, id, fields, options, dryrun=False, context=None):
        if context is None:
            context = {}
        context[CONNECTOR_IMPORT_KEY] = not dryrun
        return super(connector_base_import, self).do(cr, uid, id, fields,
                                                     options, dryrun=dryrun,
                                                     context=context)


original_load = orm.BaseModel.load


@job
def import_one_line(session, model_name, fields, line):
    model = session.pool[model_name]
    return original_load(model, session.cr, session.uid, fields, [line],
                         context=session.context)


def load(self, cr, uid, fields, data, context=None):
    if context is None:
        context = {}

    module_installed = bool(self.pool[connector_base_import_installed._name])
    connector_import = context.get(CONNECTOR_IMPORT_KEY, False)
    if module_installed and connector_import:
        for line in data:
            session = ConnectorSession(cr, uid, context)
            import_one_line.delay(session, self._name, fields, line)
        return {'messages': []}
    return original_load(self, cr, uid, fields, data, context=context)


orm.BaseModel.load = load
