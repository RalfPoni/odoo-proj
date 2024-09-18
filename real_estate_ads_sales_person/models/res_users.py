from odoo import models, fields, api

class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "sales_id", string="Properties")
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    