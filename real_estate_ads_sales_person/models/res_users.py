from odoo import models, fields, api

class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2Many("estate.property", "sales_id", string="Properties")
    