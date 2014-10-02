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

from openerp.osv import fields, orm
import simplejson


class ConnectorBuffer(orm.Model):
    _name = 'connector.buffer'
    _description = 'connector buffer'

    def _get_resource(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for connector_buffer in self.browse(cr, uid, ids, context=context):
            res[connector_buffer.id] = simplejson.dumps(connector_buffer.data)
        return res

    def _set_resource(self, cr, uid, ids, field_name, field_value, arg,
                      context=None):
        if not isinstance(ids, [list, tuple]):
            ids = [ids]
        for connector_buffer in self.browse(cr, uid, ids, context=context):
            connector_buffer.write({'data': simplejson.loads(field_value)})
        return True

    def get_data(self, cr, uid, buffer_id, model=None, context=None):
        """
        Return the data from the store, can be inherited in order
        to map the field
        """
        connectorBuffer = self.browse(cr, uid, buffer_id, context=context)
        return connectorBuffer.data

    _columns = {
        'name': fields.char('Name'),
        'data': fields.serialized('Data'),
        'data_text': fields.function(
            _get_resource,
            fnct_inv=_set_resource,
            type="text",
            string='Data'),
        }

    _defaults = {
        'name': 'buffer',
    }


class QueueJob(orm.Model):
    _inherit = 'queue.job'
    _columns = {
        'buffer_id': fields.many2one('connector.buffer', 'Buffer'),
    }

    def create(self, cr, uid, vals, context=None):
        if context.get('buffer_id'):
            vals['buffer_id'] = context['buffer_id']
        return super(QueueJob, self).create(cr, uid, vals, context=context)

    def unlink(self, cr, uid, ids, context=None):
        for job in self.browse(cr, uid, ids, context=context):
            if job.buffer_id:
                job.buffer_id.unlink()
        return super(QueueJob, self).unlink(cr, uid, ids, context=context)
