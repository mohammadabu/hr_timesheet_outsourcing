# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree
import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    outsourcing_task_id = fields.Many2one('outsourcing.task', 'Task', index=True, domain="[('company_id', '=', company_id)]")
    outsourcing_id = fields.Many2one('outsourcing.outsourcing', 'outsourcing', domain=[('allow_timesheets', '=', True)])

    @api.constrains('outsourcing_task_id', 'outsourcing_id')
    def _check_task_project(self):
        for line in self:
            if line.outsourcing_task_id and line.outsourcing_id and line.outsourcing_task_id.outsourcing_id != line.outsourcing_id:
                raise ValidationError(_(
                    "The outsourcing and the task's outsourcing are inconsistent. " +
                    "The selected task must be in the selected outsourcing."
                ))

    @api.onchange('outsourcing_id')
    def onchange_project_id(self):
        # force domain on task when project is set
        if self.outsourcing_id:
            if self.outsourcing_id != self.outsourcing_task_id.outsourcing_id:
                # reset task when changing outsourcing
                self.outsourcing_task_id = False
            return {'domain': {
                'outsourcing_task_id': [('outsourcing_id', '=', self.outsourcing_id.id)]
            }}
        return {'domain': {
            'outsourcing_task_id': [('outsourcing_id.allow_timesheets', '=', True)]
        }}


    @api.onchange('outsourcing_task_id')
    def _onchange_task_id(self):
        if not self.outsourcing_id:
            self.outsourcing_id = self.outsourcing_task_id.outsourcing_id