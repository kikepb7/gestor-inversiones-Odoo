from random import randint
from odoo import models, fields, api

# Relación Many2one de la clase Investment con res.user --> identifica al inversor responsable de la inversión
# Relación One2many de la clase Transacción con res.partner --> identifica las contrapartes en las transacciones (compradores, vendedores, etc)
# Relación Many2one de la clase Transacción e Inversión --> vincula la transacción a la inversión que afecta
# Relación Many2many de la clase Transacción o Inversión en Portfolio --> agrupa inversiones y/o transacciones en portfolios


class Investment(models.Model):
    _name = 'investment.investment'
    _description = 'Modelo para registrar las inversiones'

    name = fields.Char(string='Nombre', required=True, help='Nombre de la inversión')
    description = fields.Text(help='Descripción de la inversión')
    image = fields.Image(string='Logo de la empresa')
    amount = fields.Float(string='Cantidad de acciones', help='Cantidad de dinero invertida')
    market_price = fields.Float(string='Precio de mercado', help='Precio en el que cotiza actualmente')
    start_date = fields.Date(string='Fecha de inicio', help='Fecha de inicio de la inversión')
    end_date = fields.Date(string='Fecha de vencimiento', help='Fecha de finalización de la inversión')
    profit = fields.Float(string='Rentabilidad esperada (%)')
    risk = fields.Integer(string='Riesgo asociado (%)')
    investment_type = fields.Selection([
        ('acciones', 'Acciones'),
        ('bonos', 'Bonos'),
        ('fondos', 'Fondos'),
        ('crypto', 'Crypto'),
    ], string='Tipo de inversión', default='Otros', help='Tipo de inversión')
    total_investment = fields.Float(string='Valor total de la inversión', compute='_compute_total_investment',
                                    store=True, readonly=True)
    expected_profit = fields.Float(string='Profit no realizado', compute='_compute_expected_profit')
    expected_loss = fields.Float(string='Pérdida Esperada', compute='_compute_expected_loss')

    user_id = fields.Many2one('res.users', string='Inversor')
    transaction_ids = fields.One2many(comodel_name='investment.transaction', inverse_name='investment_id')

    # Cálculo total de la inversión
    @api.depends("amount", "market_price", "transaction_ids.value")
    def _compute_total_investment(self):
        for record in self:
            total = record.amount * record.market_price
            record.total_investment = total

    # Cálculo del profit esperado
    @api.depends('profit', 'total_investment')
    def _compute_expected_profit(self):
        for investment in self:
            investment.expected_profit = investment.total_investment * (investment.profit / 100)

    # Cálculo de la pérdida esperada
    @api.depends("amount", "market_price", "risk")
    def _compute_expected_loss(self):
        for investment in self:
            investment.expected_loss = investment.total_investment * (investment.risk / 100)


class Transaction(models.Model):
    _name = 'investment.transaction'
    _description = 'Modelo para registrar las transacciones'

    name = fields.Char(string='Título', required=True, help='Título de la transacción')
    description = fields.Text(string='Descripción')
    date = fields.Date(string='Fecha de la transacción', help='Fecha de la transacción')
    value = fields.Float(string='Cantidad')
    transaction_type = fields.Selection(
        string='Tipo de transacción',
        selection=[("buy", "Compra"), ("sell", "Venta")],
        default="buy"
    )
    commissions = fields.Float(string='Comisión')
    taxes = fields.Float(string='Impuestos')

    partner_ids = fields.Many2many(comodel_name='res.partner', string='Contrapartes')
    investment_id = fields.Many2one(comodel_name='investment.investment', string='Inversión relacionada')


class Portfolio(models.Model):
    _name = 'investment.portfolio'
    _description = 'Modelo para registrar carteras de inversión'

    name = fields.Char(string='Nombre', required=True, help='Nombre de la cartera de inversión')
    description = fields.Text(string='Descripción', help='Descripción de la cartera de inversión')
    total_value = fields.Float(string='Valor total')
    investment_objetive = fields.Text(string='Objetivo de la inversión')
    time_horizon = fields.Selection(
        string='Plazo de la inversión',
        selection=[("short", "Corto plazo"), ("medium", "Medio plazo"), ("long", "Largo plazo")],
        default='medium'
    )

    investment_ids = fields.Many2many(comodel_name='investment.investment', string='Inversiones', limit=10)
    transaction_ids = fields.Many2many(comodel_name='investment.transaction', string='Transacciones')
