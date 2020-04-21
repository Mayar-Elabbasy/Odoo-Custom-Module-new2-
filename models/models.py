# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import timedelta
from odoo.exceptions import ValidationError


class Calls(models.Model):
    _name = 'iti.calls'
    _description = 'calls'
    # _rec_name = 'start_call_time'

    start_call_time = fields.Datetime()
    stop_call_time = fields.Datetime()
    call_duration = fields.Float(compute = "_compute_duration", store=True)
    source = fields.Char()
    destination = fields.Char()
    name = fields.Char(default='New')
    station = fields.Many2one(comodel_name='iti.station')
    tags = fields.Many2many(comodel_name='iti.tags')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('invoiced', 'Invoiced'),
    ], default='draft', string='Status')
    partner_id = fields.Many2one(comodel_name='res.partner')

    @api.constrains('stop_call_time')
    def _check_stop_call_time(self):
        for record in self:
            if record.stop_call_time < record.start_call_time:
                raise ValidationError("The call stop time must be bigger that start time,"
                                      " Make sure that you enter the right time!!")
        # all records passed the test, don't return anything

    @api.depends('stop_call_time', 'start_call_time')
    def _compute_duration(self):
        for record in self:
            if(record.start_call_time and record.stop_call_time):
                record.call_duration = (record.stop_call_time - record.start_call_time).seconds / 60

    def create_invoice(self):
        invoice_object = self.env['account.move'].create({
            'partner_id': self.partner_id.id,
            'type': 'out_invoice',
        })

        invoice_line_object = self.env['account.move.line'].create({
            'name': 'call cost',
            'move_id': invoice_object.id,
            'price_unit': self.call_duration * 0.30,
            'account_id': self.partner_id.property_account_receivable_id.id,
        })

    class Station(models.Model):
        _name = 'iti.station'
        name = fields.Char()
        calls = fields.One2many(comodel_name='iti.calls', inverse_name='station')

    class Tags(models.Model):
        _name = 'iti.tags'
        name = fields.Char()

        #to run it use
        # ~ / odoo / odoo - 13.0.post20200414 / odoo.py - -db_host = localhost - -db_user = odoo - -db_password = odoo - -db_port = 5432 - -addons - path = ~  / odoo / odoo - 13.0.post20200414 / myaddons /