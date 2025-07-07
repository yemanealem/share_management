from odoo import models, fields, api

class Shareholder(models.Model):
    _name = 'share_management.shareholder'
    _description = 'Shareholder'

    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    total_shares = fields.Integer(compute='_compute_totals', store=True)
    total_invested = fields.Monetary(compute='_compute_totals', store=True, currency_field='currency_id')
    share_percent = fields.Float(compute='_compute_share_percent', store=True)
    dividend_received = fields.Monetary(compute='_compute_dividend_received', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)

    transaction_ids = fields.One2many('share_management.share_transaction', 'shareholder_id', string='Transactions')
    dividend_ids = fields.One2many('share_management.share_dividend', 'shareholder_id', string='Dividends')

    @api.depends('transaction_ids.quantity', 'transaction_ids.type', 'transaction_ids.amount')
    def _compute_totals(self):
        for shareholder in self:
            total_shares = 0
            total_invested = 0.0
            for tx in shareholder.transaction_ids:
                if tx.type == 'buy':
                    total_shares += tx.quantity
                    total_invested += tx.amount
                elif tx.type == 'sell':
                    total_shares -= tx.quantity
                    total_invested -= tx.amount
                elif tx.type == 'transfer':
                    if tx.shareholder_id == shareholder:
                        total_shares -= tx.quantity
                    if tx.receiver_id == shareholder:
                        total_shares += tx.quantity
            shareholder.total_shares = total_shares
            shareholder.total_invested = total_invested

    @api.depends('total_shares')
    def _compute_share_percent(self):
        total_all_shares = sum(self.env['share_management.shareholder'].search([]).mapped('total_shares'))
        for shareholder in self:
            shareholder.share_percent = (shareholder.total_shares / total_all_shares * 100) if total_all_shares > 0 else 0

    @api.depends('dividend_ids.amount')
    def _compute_dividend_received(self):
        for shareholder in self:
            shareholder.dividend_received = sum(shareholder.dividend_ids.mapped('amount'))
