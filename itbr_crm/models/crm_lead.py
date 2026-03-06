# Copyright 2023 - TODAY, IT Brasil
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    parent_id = fields.Many2one(
        related="partner_id.parent_id",
        readonly=True,
    )

    country_enforce_cities = fields.Boolean(
        related="partner_id.country_id.enforce_cities"
    )

    street_name = fields.Char(compute="_compute_address", inverse="_inverse_br_address_data")
    street_number = fields.Char(compute="_compute_address", inverse="_inverse_br_address_data")
    street_number2 = fields.Char(compute="_compute_address", inverse="_inverse_br_address_data")
    city_id = fields.Many2one(
        "res.city", compute="_compute_address", inverse="_inverse_br_address_data"
    )

    @api.depends("street")
    def _compute_address(self):
        super()._compute_address()
        for lead in self:
            partner = lead.partner_id
            lead.update(
                {
                    "street_name": partner.street_name,
                    "street_number": partner.street_number,
                    "street_number2": partner.street_number2,
                    "city_id": partner.city_id,
                }
            )

    def _inverse_br_address_data(self):
        for lead in self:
            lead.partner_id.write(
                {
                    "street_name": lead.street_name,
                    "street_number": lead.street_number,
                    "street_number2": lead.street_number2,
                    "city_id": lead.city_id.id,
                }
            )
