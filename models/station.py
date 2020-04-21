# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Station(models.Model):
    _name = 'iti.station'

    name = fields.Char()
    calls = fields.One2many(comodel_name='iti.calls', inverse_name='station')