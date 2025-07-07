from odoo import models, fields,api

class ShareTransaction(models.Model):
    _name = 'share_management.share_transaction'
    _description = 'Share Transaction'

    type = fields.Selection([
    ('buy', 'Buy'),
    ('sell', 'Sell'),
    ('transfer', 'Transfer')
        ], required=True)
    quantity = fields.Integer(required=True)
    price_per_share = fields.Float(required=True)
    amount = fields.Monetary(compute='_compute_amount', store=True, currency_field='currency_id')
    receiver_id = fields.Many2one('share_management.shareholder', string='Receiver')  # optional, for transfers
    date = fields.Date()
    shareholder_id = fields.Many2one('share_management.shareholder', string='Shareholder')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)


    @api.depends('quantity', 'price_per_share')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.quantity * rec.price_per_share
