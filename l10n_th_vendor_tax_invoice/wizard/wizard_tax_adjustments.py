# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import models, fields, api


class TaxAdjustments(models.TransientModel):
    _inherit = 'tax.adjustments.wizard'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
    )
    tax_date = fields.Date()
    tax_invoice = fields.Char(
        string='Tax Invoice Number',
    )
    amount_tax_base = fields.Monetary(
        string='Tax Base',
        currency_field='company_currency_id',
        required=True,
    )

    @api.multi
    def _create_move(self):
        res = super()._create_move()
        move_line = self.env['account.move.line'].search(
            [('move_id', '=', res)])
        for line in move_line:
            line.partner_id = self.partner_id
            line.tax_invoice_manual = self.tax_invoice
            line.tax_date_manual = self.tax_date
            line.tax_base_amount = self.amount_tax_base
        return res