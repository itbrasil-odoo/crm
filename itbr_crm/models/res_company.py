# Copyright 2026 - TODAY, IT Brasil
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    type = fields.Selection(related="partner_id.type")

    country_enforce_cities = fields.Boolean(
        related="partner_id.country_id.enforce_cities",
        readonly=True,
    )

    street_name = fields.Char(compute="_compute_address", inverse="_inverse_br_address_data")
    street_number = fields.Char(compute="_compute_address", inverse="_inverse_br_address_data")
    street_number2 = fields.Char(compute="_compute_address", inverse="_inverse_br_address_data")
    city_id = fields.Many2one(
        "res.city", compute="_compute_address", inverse="_inverse_br_address_data"
    )

    @api.depends(
        lambda self: [
            "partner_id.%s" % fname
            for fname in self._get_company_address_field_names()
        ]
        + ["partner_id.street_number2"]
    )
    def _compute_address(self):
        # res.company DOES have _compute_address in its Python MRO (core
        # res.company + l10n_br_base via _inherit); calling super() populates
        # the core/l10n_br address fields (street, city, zip, state_id,
        # country_id, district, ...). Without it those stay empty, country_id
        # is lost and show_l10n_br becomes False, hiding the whole address.
        super()._compute_address()
        for company in self:
            partner = company.partner_id
            company.update(
                {
                    "street_name": partner.street_name,
                    "street_number": partner.street_number,
                    "street_number2": partner.street_number2,
                    "city_id": partner.city_id,
                }
            )

    def _inverse_br_address_data(self):
        for company in self:
            company.partner_id.write(
                {
                    "street_name": company.street_name,
                    "street_number": company.street_number,
                    "street_number2": company.street_number2,
                    "city_id": company.city_id.id,
                }
            )
