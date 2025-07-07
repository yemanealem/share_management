from odoo import models, fields

class ShareDividend(models.Model):
    _name = 'share_management.share_dividend'
    _description = 'Share Dividend'

    shareholder_id = fields.Many2one('share_management.shareholder', string='Shareholder', required=True)
    amount = fields.Monetary(string='Amount', required=True, currency_field='currency_id')
    date = fields.Date(string='Date', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)
