# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


# Faktur Pajak
#   Constraint Unik Nomor Faktur
#   Constraint Nomor Faktur Pajak
#   Many2one Invoice
#   One2one Onchange
#   Domain Available
#   Wizard Generator
#   State Computed invoice_id
#   Related
#   Custom Report Invoice

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    faktur_id = fields.Many2one('account.faktur', 'Faktur Pajak')
    state = fields.Selection(selection_add=[('complete', 'Complete')])

    @api.multi
    def action_complete(self):
        for invoice in self :
            if invoice.state == 'paid' and invoice.faktur_id:
                invoice.state = 'complete'
            else:
                raise ValidationError('Mohon invoice dibayar dan melengkapi informasi faktur pajak sebelum complete invoice')


    @api.multi
    def write(self, values):
        result = super(AccountInvoice, self).write(values)

        for invoice in self:
            faktur = self.env['account.faktur'].search([('invoice_id', '=', invoice.id)])
            if faktur :
                faktur.write({
                    'invoice_id' : False
                })
            if invoice.faktur_id:
                # import ipdb; ipdb.set_trace()
                # invoice.faktur_id Record Fakturnya (account.faktur,1)
                # invoice.faktur_id.name Nomor Fakturnya '123-00-001'
                # invoice.faktur_id.name = '123-01-88888888'
                # invoice.faktur_id.invoice_id = 1
                # invoice.faktur_id.invoice_id = invoice.id
                invoice.faktur_id.available = False
                invoice.faktur_id.invoice_id = invoice.id

        return result

class FakturPajak(models.Model):
    _name = 'account.faktur'

    name = fields.Char('Name', required=True)
    available = fields.Boolean('Available', default=True)
    invoice_id = fields.Many2one('account.invoice', 'Invoice')
    invoice_number = fields.Char('Nomor Invoice', related='invoice_id.number')
    partner_name = fields.Char('Nama Partner', related='invoice_id.partner_id.name')
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Nomor Faktur Harus Unik!'),
    ]
    state = fields.Selection([
            ('available','Available'),
            ('taken', 'Taken'),
        ], string='Status', index=True, readonly=True, default='available',
        track_visibility='onchange', copy=False, compute='_compute_state', store=True)
    
    @api.depends('invoice_id')
    def _compute_state(self):
        for faktur in self:
            if faktur.invoice_id:
                faktur.state = 'taken'
            else:
                faktur.state = 'available'

    @api.one
    @api.constrains('name')
    def _check_format_name(self):
        # xxx-xx-xxxxxxxx
        if self.name:
            list_str_name = self.name.split("-")
            if len(list_str_name) == 3:
                for str_name in list_str_name:
                    if not str_name.isdigit():
                        raise ValidationError("Nomor Faktur Haru Memiliki Format XXX-XX-XXXXXXXX!")
            else:
                raise ValidationError("Nomor Faktur Haru Memiliki Format XXX-XX-XXXXXXXX!")

    def action_open_wizard_simple(self):
        return {
            'name': 'Transfer',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.faktur.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context' : {}
        }