from odoo import fields, models, api

# Decorators can be found in property_offer.py

class Property(models.Model):
    _name = "estate.property"
    _inherit = ['mail.thread']
    _description = "Estate properties"

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([('new', 'New'), ('sold', 'Sold'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('cancel', 'Cancel')],
                             default='new', String="Status")
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available from")
    expected_price = fields.Monetary(string="Expected price")
    selling_price = fields.Monetary(string="Selling price")
    bedroom = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Areas")
    facade = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Float(string="Garden area")
    garden_orientation = fields.Selection([
        ('north', 'North'), ('south', 'South'),
         ('east', 'East'), ('west', 'West')],
        string="Garden orientation", default='north')

    # One property goes to many offers
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    # Many properties go to many sellers
    sales_id = fields.Many2one('res.users', string='Seller')
    buyer_id = fields.Many2one('res.partner', string='Buyer', domain=[('is_company', '=', True)])
    total_area = fields.Integer(string='Total Area', compute='_compute_total_area')
    phone = fields.Char(string="Phone", related="buyer_id.phone")
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'cancel'

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for rec in self:
            if len(rec.offer_ids) > 0:

                max_offer = max(rec.offer_ids, key=lambda offer_id: offer_id.price)
                # This can also be done with max(rec.offer_ids.mapped('price'))
                rec.best_offer = max_offer.price

            else:
                rec.best_offer = 0

    offer_count = fields.Integer(string="Offer Count", compute='_compute_offer_count')
    best_offer = fields.Monetary(string="Best Offer", compute='_compute_best_offer')

    def action_property_view_offers(self):
        return {
            'type' : 'ir.actions.act_window',
            'name' : f"{self.name} - Offers",
            'domain' : [('property_id', '=', self.id)],
            'view_mode' : 'tree',
            'res_model' : 'estate.property.offer'

            # To use this function for a smart button you would set the name of the button
            # in the div to action_property_view_offers without the % and brackets, and you would change
            # the button type to object instead of action, that is all that would be changed
        }

    def action_url_action(self):
        return {
            'type' : 'ir.actions.act_url',
            'url' : 'https://google.com',
            # New opens new tab, self opens on the same tab
            'target' : 'new'
        }

    def _get_report_base_filename(self):
        # Ensure one ensures that we get only one record from a query, it is available in all models we create
        self.ensure_one()
        return 'Estate Property - %s' % (self.name)

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property types description"

    name = fields.Char(string="Name", required=True)

class PropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Property tags description"


    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string='Color')