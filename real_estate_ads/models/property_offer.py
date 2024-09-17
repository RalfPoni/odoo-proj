from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError

# 3 types of models, Abstract, Transient, Default
class AbstractOffer(models.AbstractModel):
    _name = 'abstract.model.offer'
    _description = 'Abstract model'

    partner_email = fields.Char(string='Email')
    partner_phone = fields.Char(string='Phone number')

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _inherit = ['abstract.model.offer']
    _description = "Estate property offers"

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.property_id.name} - {rec.partner_id.name}"
            else:
                rec.name = False

    name = fields.Char(string="Description", compute='_compute_name')
    price = fields.Float(String="Price", required=True, default=0)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estate.property', string="Property")
    @api.model
    def _set_creation_date(self):
        return fields.Date.today()

    def action_accept_offer(self):
        self.validate_accepted_offer()
        self.status = 'accepted'
        self.property_id.write({
            'selling_price' : self.price,
            'state' : 'accepted'
        })

    def validate_accepted_offer(self):
        offer_ids = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted')
        ])

        if offer_ids:
            raise ValidationError("You have already accepted an offer! You need to decline your accepted offer before you can accept another offer.")

    def action_reject_offer(self):
        self.status = 'refused'
        if all(offer_id.status == 'refused' for offer_id in self.property_id.offer_ids):
            self.property_id.write({
                'selling_price': 0,
                'state': 'received'
            })

    create_date = fields.Date(string="Create Date", default=_set_creation_date)
    validity = fields.Integer(string="Validity", default=7)
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline')

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.create_date and rec.validity:
                rec.deadline = rec.create_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    @api.depends('validity', 'create_date')
    def _inverse_deadline(self):
        for rec in self:
            rec.validity = (rec.deadline - rec.create_date).days

    def extend_offer_deadline(self):
        activ_ids = self._context.get('active_ids', [])
        print(activ_ids)
        if activ_ids:
           offer_ids = self.env['estate.property.offer'].browse(activ_ids)
           for offer in offer_ids:
               offer.validity += 1

    def _extend_offer_deadline(self):
        offer_ids = self.env['estate.property.offer'].search([])
        for offer in offer_ids:
            offer.validity += 1



    # @api.autovacuum
    # def _clean_offers(self): # Self means I already have access to this model
    #     self.search([('status','=','refused')]).unlink()

    # This decorator allows the creation of records from dictionaries or a list of dictionaries
    # the values are passed as parameters to the method, you can also update the values before they have been created
    # this decorator is mostly used with the "Create" function which is the ORM method and it takes another parameter
    # which can vals or values
    # @api.model_create_multi
    # def create(self, vals):
    #     for rec in vals:
    #         if not rec.get('create_date'):
    #             rec['create_date'] = fields.Date.today()
    #     return super(PropertyOffer, self).create(vals)

    # C onstraints decorator is supposed to prevent a particular operation from happening
    # when certain conditions are met. The decorator takes an argument, a field on which you want
    # to perform a constraint. If the field is in the view and is in the create or write call
    # @api.constrains('validity')
    # def _check_validity(self):
    #     for rec in self:
    #         if rec.deadline <= rec.create_date:
    #             raise ValidationError("Deadline cannot be before creation date")

    # def write(self, vals):
    #     print(vals)
    #     #self.env('res.partner').browse(1) will give res.partner(1)
    #     res_partner_ids = self.env['res.partner'].search([('is_company', '=', True)]) #There is also search count which just returns the number of matches
    #     print(res_partner_ids)
    #     return super(PropertyOffer, self).write(vals)